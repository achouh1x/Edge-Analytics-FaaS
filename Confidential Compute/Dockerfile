FROM ubuntu:16.04

RUN apt-get update &&  apt-get -y install g++

WORKDIR .

ARG GRAPHENE_INSTALL_DIR 

ENV DAAL_INSTALL_DIR /opt/intel/daal
ENV GRAPHENE_INSTALL_DIR $GRAPHENE_INSTALL_DIR

#Install DAAL
ADD https://github.com/intel/daal/releases/download/2019_u3/l_daal_oss_p_2019.3.006.tgz .
RUN mkdir -p $DAAL_INSTALL_DIR
RUN tar -zxf l_daal_oss_p_2019.3.006.tgz -C $DAAL_INSTALL_DIR

#Set DAAL environment variables
RUN /bin/bash -c "source $DAAL_INSTALL_DIR/l_daal_oss_p_2019.3.006/daal_prebuild/linux/daal/bin/daalvars.sh intel64"
ENV DAALROOT $DAAL_INSTALL_DIR/l_daal_oss_p_2019.3.006/daal_prebuild/linux/daal

#Build SVM Application
RUN g++ $DAALROOT/examples/cpp/source/svm/svm_two_class_csr_batch.cpp -o $DAALROOT/examples/cpp/svm_two_class_csr_batch -I$DAALROOT/include -I$DAALROOT/examples/cpp/source/utils/ -L$DAALROOT/lib/intel64_lin $DAALROOT/lib/intel64_lin/libdaal_core.a $DAALROOT/lib/intel64_lin/libdaal_sequential.a -lpthread -lm -ldl

ENV LD_LIBRARY_PATH $DAALROOT/lib/intel64_lin:$DAALROOT/../tbb/lib/intel64_lin/gcc4.4:$LD_LIBRARY_PATH

#Copy binary, datasets to graphene working directory
RUN mkdir -p $GRAPHENE_INSTALL_DIR/LibOS/shim/test/apps/data/batch
RUN mkdir -p $GRAPHENE_INSTALL_DIR/LibOS/shim/test/apps/svm 

RUN cp $DAALROOT/examples/cpp/svm_two_class_csr_batch $GRAPHENE_INSTALL_DIR/LibOS/shim/test/apps/svm
RUN cp $DAALROOT/examples/data/batch/svm_two_class_test_csr.csv $GRAPHENE_INSTALL_DIR/LibOS/shim/test/apps/data/batch
RUN cp $DAALROOT/examples/data/batch/svm_two_class_test_labels.csv $GRAPHENE_INSTALL_DIR/LibOS/shim/test/apps/data/batch
RUN cp $DAALROOT/examples/data/batch/svm_two_class_train_csr.csv $GRAPHENE_INSTALL_DIR/LibOS/shim/test/apps/data/batch
RUN cp $DAALROOT/examples/data/batch/svm_two_class_train_labels.csv $GRAPHENE_INSTALL_DIR/LibOS/shim/test/apps/data/batch
