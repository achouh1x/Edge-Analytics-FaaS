ARG UBUNTU_VERSION=16.04
FROM ubuntu:$UBUNTU_VERSION

WORKDIR /code
ARG UBUNTU_VERSION
ARG MY_ROOT=/code
ARG DEVICE=CPU_FP32
ARG ONNXRUNTIME_REPO=https://github.com/microsoft/onnxruntime
ARG ONNXRUNTIME_BRANCH=master
ARG OV_VERSION=2020.3.194

ENV LD_LIBRARY_PATH=/opt/miniconda/lib:/usr/lib:/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
ENV INTEL_OPENVINO_DIR=/opt/intel/openvino_${OV_VERSION}
ENV InferenceEngine_DIR=${INTEL_OPENVINO_DIR}/deployment_tools/inference_engine/share
ENV IE_PLUGINS_PATH=${INTEL_OPENVINO_DIR}/deployment_tools/inference_engine/lib/intel64
ENV ngraph_DIR=${INTEL_OPENVINO_DIR}/deployment_tools/ngraph/
ENV LD_LIBRARY_PATH=/opt/intel/opencl:${INTEL_OPENVINO_DIR}/inference_engine/external/gna/lib:${INTEL_OPENVINO_DIR}/deployment_tools/inference_engine/external/mkltiny_lnx/lib:${ngraph_DIR}/lib:${INTEL_OPENVINO_DIR}/deployment_tools/inference_engine/external/omp/lib:${INTEL_OPENVINO_DIR}/deployment_tools/inference_engine/external/tbb/lib:${IE_PLUGINS_PATH}:${LD_LIBRARY_PATH}
ENV OpenCV_DIR=${INTEL_OPENVINO_DIR}/opencv/share/OpenCV
ENV LD_LIBRARY_PATH=${INTEL_OPENVINO_DIR}/opencv/lib:${INTEL_OPENVINO_DIR}/opencv/share/OpenCV/3rdparty/lib:${LD_LIBRARY_PATH}
ENV HDDL_INSTALL_DIR=${INTEL_OPENVINO_DIR}/deployment_tools/inference_engine/external/hddl
ENV LD_LIBRARY_PATH=${INTEL_OPENVINO_DIR}/deployment_tools/inference_engine/external/hddl/lib:$LD_LIBRARY_PATH
ENV LANG en_US.UTF-8
ENV PATH /opt/cmake/bin:$PATH

RUN if [ "$UBUNTU_VERSION" = "18.04" ]; \
    then export LIBBOOST="libboost-filesystem1.65-dev libboost-thread1.65-dev"; export OV_APT="intel-openvino-dev-ubuntu18-${OV_VERSION}"; \
    else export LIBBOOST="libboost-filesystem1.58.0 libboost-thread1.58.0"; export OV_APT="intel-openvino-dev-ubuntu16-${OV_VERSION}"; \
    fi && \
    apt update && \
    apt -y install apt-transport-https ca-certificates python3.5 python3-pip zip x11-apps lsb-core wget cpio sudo $LIBBOOST libboost-python-dev libpng-dev zlib1g-dev git libnuma1 ocl-icd-libopencl1 clinfo protobuf-compiler libprotoc-dev autoconf automake libtool libjson-c-dev && \
    rm -rf /var/lib/apt/lists/* && \
    wget https://github.com/intel/compute-runtime/releases/download/19.15.12831/intel-gmmlib_19.1.1_amd64.deb && \
    wget https://github.com/intel/compute-runtime/releases/download/19.15.12831/intel-igc-core_1.0.2-1787_amd64.deb && \
    wget https://github.com/intel/compute-runtime/releases/download/19.15.12831/intel-igc-opencl_1.0.2-1787_amd64.deb && \
    wget https://github.com/intel/compute-runtime/releases/download/19.15.12831/intel-opencl_19.15.12831_amd64.deb && \
    wget https://github.com/intel/compute-runtime/releases/download/19.15.12831/intel-ocloc_19.15.12831_amd64.deb && \
    dpkg -i *.deb && rm -rf *.deb && \
    locale-gen en_US.UTF-8 && update-locale LANG=en_US.UTF-8 && \
    pip3 install cython numpy==1.18.4 && \
    mkdir -p /opt/cmake/bin && \
    cd ${MY_ROOT} && \
    wget https://github.com/Kitware/CMake/releases/download/v3.13.2/cmake-3.13.2-Linux-x86_64.tar.gz && \
    tar -xf cmake-3.13.2-Linux-x86_64.tar.gz --strip 1 -C /opt/cmake && rm -rf ${MY_ROOT}/cmake-3.13.2-Linux-x86_64.tar.gz && \
    wget https://apt.repos.intel.com/openvino/2020/GPG-PUB-KEY-INTEL-OPENVINO-2020 && \
    apt-key add GPG-PUB-KEY-INTEL-OPENVINO-2020 && \
    cd /etc/apt/sources.list.d && \
    echo "deb https://apt.repos.intel.com/openvino/2020 all main">intel-openvino-2020.list && \ 
    apt update && \
    #search the pacakges available for new version
    #apt-cache search intel-openvino-dev-ubuntu18 
    apt -y install $OV_APT && \
    cd /opt/intel/openvino_${OV_VERSION}/install_dependencies && ./install_openvino_dependencies.sh && \
    cd ${MY_ROOT} && \
    git clone --recursive -b $ONNXRUNTIME_BRANCH $ONNXRUNTIME_REPO && \
    sed -i "s/sudo//" onnxruntime/dockerfiles/scripts/install_common_deps.sh && \
    /bin/sh onnxruntime/dockerfiles/scripts/install_common_deps.sh && \
    cd onnxruntime/cmake/external/onnx && python3 setup.py install && \
    cd ${MY_ROOT}/onnxruntime && ./build.sh --config Release --update --build --parallel --use_openvino $DEVICE --build_wheel --use_full_protobuf && \
    pip3 install build/Linux/Release/dist/*-linux_x86_64.whl && \
    cd ${MY_ROOT}/ && rm -rf cmake-3.14.3-Linux-x86_64 onnxruntime && \
    cd ${INTEL_OPENVINO_DIR} && rm -rf documentation && cd deployment_tools/ && rm -rf model_optimizer open_model_zoo demo && cd inference_engine && rm -rf samples