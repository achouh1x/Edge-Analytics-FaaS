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
    apt -y install python3.5 python3-pip zip x11-apps lsb-core wget cpio sudo libboost-python-dev libpng-dev zlib1g-dev git libnuma1 ocl-icd-libopencl1 clinfo libboost-filesystem1.58.0 libboost-thread1.58.0 protobuf-compiler libprotoc-dev && pip3 install numpy networkx opencv-python pytest && locale-gen en_US.UTF-8 && update-locale LANG=en_US.UTF-8

ENV pattern="COMPONENTS=DEFAULTS"
ENV replacement="COMPONENTS=intel-openvino-ie-sdk-ubuntu-xenial__x86_64;intel-openvino-ie-rt-cpu-ubuntu-xenial__x86_64;intel-openvino-ie-rt-gpu-ubuntu-xenial__x86_64;intel-openvino-ie-rt-vpu-ubuntu-xenial__x86_64;intel-openvino-ie-rt-hddl-ubuntu-xenial__x86_64;intel-openvino-model-optimizer__x86_64;intel-openvino-opencv-lib-ubuntu-xenial__x86_64"
COPY l_openvino_*.tgz .
RUN tar -xzf l_openvino_toolkit*.tgz && \
    rm -rf l_openvino_toolkit*.tgz && \
    cd l_openvino_toolkit* && \
    sed -i "s/$pattern/$replacement/" silent.cfg && \
    sed -i 's/decline/accept/g' silent.cfg && \
    ./install.sh -s silent.cfg && \
    /bin/bash -c "source /opt/intel/computer_vision_sdk/bin/setupvars.sh" && \
    ./install_cv_sdk_dependencies.sh && \
    cd - && \
    rm -rf l_openvino_toolkit*

ENV LD_LIBRARY_PATH=/usr/lib:/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
ENV INTEL_OPENVINO_DIR=/opt/intel/openvino_2019.3.334
ENV INTEL_CVSDK_DIR=/opt/intel/openvino_2019.3.334
ENV LD_LIBRARY_PATH=${INTEL_OPENVINO_DIR}/deployment_tools/model_optimizer/model_optimizer_caffe/bin:${LD_LIBRARY_PATH}
ENV ModelOptimizer_ROOT_DIR=${INTEL_OPENVINO_DIR}/deployment_tools/model_optimizer/model_optimizer_caffe
ENV InferenceEngine_DIR=${INTEL_CVSDK_DIR}/deployment_tools/inference_engine/share
ENV IE_PLUGINS_PATH=${INTEL_CVSDK_DIR}/deployment_tools/inference_engine/lib/intel64
ENV LD_LIBRARY_PATH=/opt/intel/opencl:${INTEL_OPENVINO_DIR}/deployment_tools/inference_engine/external/cldnn/lib:${INTEL_OPENVINO_DIR}/inference_engine/external/gna/lib:${INTEL_OPENVINO_DIR}/deployment_tools/inference_engine/external/mkltiny_lnx/lib:${INTEL_OPENVINO_DIR}/deployment_tools/inference_engine/external/omp/lib:${INTEL_OPENVINO_DIR}/deployment_tools/inference_engine/external/tbb/lib:${IE_PLUGINS_PATH}:${LD_LIBRARY_PATH}
ENV OpenCV_DIR=${INTEL_OPENVINO_DIR}/opencv/share/OpenCV
ENV LD_LIBRARY_PATH=${INTEL_OPENVINO_DIR}/opencv/lib:${INTEL_OPENVINO_DIR}/opencv/share/OpenCV/3rdparty/lib:${LD_LIBRARY_PATH}
ENV PATH=${INTEL_CVSDK_DIR}/deployment_tools/model_optimizer:$PATH
ENV PYTHONPATH=${INTEL_CVSDK_DIR}/deployment_tools/model_optimizer:$PYTHONPATH
ENV PYTHONPATH=$INTEL_CVSDK_DIR/python/python3.5:${INTEL_CVSDK_DIR}/python/python3.5/ubuntu16:${PYTHONPATH}
ENV HDDL_INSTALL_DIR=${INTEL_OPENVINO_DIR}/deployment_tools/inference_engine/external/hddl
ENV LD_LIBRARY_PATH=${INTEL_OPENVINO_DIR}/deployment_tools/inference_engine/external/hddl/lib:$LD_LIBRARY_PATH

RUN wget https://github.com/intel/compute-runtime/releases/download/19.15.12831/intel-gmmlib_19.1.1_amd64.deb
RUN wget https://github.com/intel/compute-runtime/releases/download/19.15.12831/intel-igc-core_1.0.2-1787_amd64.deb
RUN wget https://github.com/intel/compute-runtime/releases/download/19.15.12831/intel-igc-opencl_1.0.2-1787_amd64.deb
RUN wget https://github.com/intel/compute-runtime/releases/download/19.15.12831/intel-opencl_19.15.12831_amd64.deb
RUN wget https://github.com/intel/compute-runtime/releases/download/19.15.12831/intel-ocloc_19.15.12831_amd64.deb

RUN sudo dpkg -i *.deb && rm -rf *.deb

ARG DEVICE=CPU_FP32
ARG ONNXRUNTIME_REPO=https://github.com/intel/onnxruntime
ARG ONNXRUNTIME_BRANCH=preview-v0.8.1

RUN mkdir -p /opt/cmake/bin

ENV PATH /opt/cmake/bin:$PATH
ENV LANG en_US.UTF-8
RUN wget https://github.com/Kitware/CMake/releases/download/v3.13.2/cmake-3.13.2-Linux-x86_64.tar.gz && \
    tar -xf cmake-3.13.2-Linux-x86_64.tar.gz --strip 1 -C /opt/cmake && rm -rf /cmake-3.13.2-Linux-x86_64.tar.gz

RUN git clone --recursive -b $ONNXRUNTIME_BRANCH $ONNXRUNTIME_REPO /onnxruntime && \
    cd /onnxruntime/cmake/external/onnx && python3 setup.py install && \
    cd /onnxruntime && ./build.sh --config RelWithDebInfo --update --build --parallel --use_openvino $DEVICE --build_wheel && pip3 install /onnxruntime/build/Linux/RelWithDebInfo/dist/*-linux_x86_64.whl && rm -rf /onnxruntime

RUN pip3 install pytest && locale-gen en_US.UTF-8 && update-locale LANG=en_US.UTF-8


