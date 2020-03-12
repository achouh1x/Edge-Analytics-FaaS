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

FROM openvino:latest

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