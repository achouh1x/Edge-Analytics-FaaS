# BSD 3-clause "New" or "Revised" license
#
# Copyright (C) 2018 Intel Coporation.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
FROM ubuntu:16.04

RUN apt update && \
    apt -y install python3.5 python3-pip zip x11-apps lsb-core wget cpio sudo libboost-python-dev libpng-dev zlib1g-dev git libnuma1 ocl-icd-libopencl1 clinfo libboost-filesystem1.58.0 libboost-thread1.58.0 protobuf-compiler libprotoc-dev && pip3 install numpy networkx opencv-python pytest cython && locale-gen en_US.UTF-8 && update-locale LANG=en_US.UTF-8

ENV pattern="COMPONENTS=DEFAULTS"
ENV replacement="COMPONENTS=intel-openvino-ie-sdk-ubuntu-xenial__x86_64;intel-openvino-ie-rt-cpu-ubuntu-xenial__x86_64;intel-openvino-ie-rt-gpu-ubuntu-xenial__x86_64;intel-openvino-ie-rt-vpu-ubuntu-xenial__x86_64;intel-openvino-ie-rt-hddl-ubuntu-xenial__x86_64;intel-openvino-model-optimizer__x86_64;intel-openvino-opencv-lib-ubuntu-xenial__x86_64"
COPY openvino_04_05_drop.tar.gz .
RUN tar -xzf openvino_04_05_drop.tar.gz && \
    rm -rf openvino_04_05_drop.tar.gz && \
    cd /openvino_04_05_drop/install_dependencies  && dpkg -i *.deb && \
    pip3 install networkx==2.3 test-generator==0.1.1 defusedxml>=0.5.0


ENV LD_LIBRARY_PATH=/opt/miniconda/lib:/usr/lib:/usr/lib/x86_64-linux-gnu:/opt/intel/opencl:$LD_LIBRARY_PATH
ENV INTEL_CVSDK_DIR=/openvino_04_05_drop
ENV INTEL_OPENVINO_DIR=/openvino_04_05_drop
ENV OPENVINO_LIB_DIR=$INTEL_CVSDK_DIR/deployment_tools/inference_engine/lib/intel64
ENV OPENVINO_NGRAPH_LIB_DIR=$INTEL_CVSDK_DIR/lib
ENV OPENVINO_TBB_LIB_DIR=$INTEL_CVSDK_DIR/deployment_tools/inference_engine/external/tbb/lib
ENV OPENVINO_MKL_TINY_LIB_DIR=$INTEL_CVSDK_DIR/deployment_tools/inference_engine/external/mkltiny_lnx/lib
ENV HDDL_INSTALL_DIR=$INTEL_CVSDK_DIR/deployment_tools/inference_engine/external/hddl
ENV InferenceEngine_DIR=$INTEL_CVSDK_DIR/deployment_tools/inference_engine/share
ENV LD_LIBRARY_PATH=$OPENVINO_LIB_DIR:$OPENVINO_NGRAPH_LIB_DIR:$OPENVINO_TBB_LIB_DIR:$OPENVINO_MKL_TINY_LIB_DIR:$LD_LIBRARY_PATH:$INTEL_CVSDK_DIR/deployment_tools/inference_engine/external/hddl/lib
RUN locale-gen en_US.UTF-8 && update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8


ARG DEVICE=CPU_FP32
ARG ONNXRUNTIME_REPO=https://github.com/intel/onnxruntime
ARG ONNXRUNTIME_BRANCH=openvino-ep-v2

RUN mkdir -p /opt/cmake/bin

ENV PATH /opt/cmake/bin:$PATH
ENV LANG en_US.UTF-8
RUN wget https://github.com/Kitware/CMake/releases/download/v3.13.2/cmake-3.13.2-Linux-x86_64.tar.gz && \
    tar -xf cmake-3.13.2-Linux-x86_64.tar.gz --strip 1 -C /opt/cmake && rm -rf /cmake-3.13.2-Linux-x86_64.tar.gz

RUN git clone --recursive -b $ONNXRUNTIME_BRANCH $ONNXRUNTIME_REPO && \
    sed -i "s/sudo//" /onnxruntime/dockerfiles/scripts/install_common_deps.sh &&\
    /bin/sh /onnxruntime/dockerfiles/scripts/install_common_deps.sh &&\
    cd /onnxruntime/cmake/external/onnx && python3 setup.py install 

RUN cd /onnxruntime && ./build.sh --config RelWithDebInfo --update --build --parallel --use_openvino $DEVICE --build_wheel

RUN cd /onnxruntime/build/Linux/RelWithDebInfo && pip3 install  dist/*-linux_x86_64.whl && cd onnxruntime/capi && cp plugins.xml /usr/local/lib/python3.5/dist-packages/onnxruntime/capi/

RUN pip3 install pytest && locale-gen en_US.UTF-8 && update-locale LANG=en_US.UTF-8