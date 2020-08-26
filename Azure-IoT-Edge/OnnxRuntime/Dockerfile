ARG UBUNTU_VERSION=16.04
ARG OV_VERSION=2020.4

FROM ubuntu:$UBUNTU_VERSION AS base

FROM base AS ov-2020.4
ENV INTEL_OPENVINO_DIR=/opt/intel/openvino_2020.4.287

FROM base AS ov-2020.3
ENV INTEL_OPENVINO_DIR=/opt/intel/openvino_2020.3.194

FROM base AS ov-2020.2
ENV INTEL_OPENVINO_DIR=/opt/intel/openvino_2020.2.130

FROM ov-${OV_VERSION} AS final

WORKDIR /code
ARG UBUNTU_VERSION
ARG OV_VERSION
ARG MY_ROOT=/code
ARG DEVICE=CPU_FP32
ARG ONNXRUNTIME_REPO=https://github.com/microsoft/onnxruntime
ARG ONNXRUNTIME_BRANCH=master

ENV LD_LIBRARY_PATH=/opt/miniconda/lib:/usr/lib:/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
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

# Set up OS version specific packages and drivers
RUN if [ "$UBUNTU_VERSION" = "18.04" ]; \
    then export LIBBOOST="libboost-filesystem1.65-dev libboost-thread1.65-dev"; \
        export OV_APT="intel-openvino-dev-ubuntu18-${OV_VERSION}"; \
        export gmmlib="https://github.com/intel/compute-runtime/releases/download/19.41.14441/intel-gmmlib_19.3.2_amd64.deb"; \
        export igc_core="https://github.com/intel/compute-runtime/releases/download/19.41.14441/intel-igc-core_1.0.2597_amd64.deb"; \
        export igc_opencl="https://github.com/intel/compute-runtime/releases/download/19.41.14441/intel-igc-opencl_1.0.2597_amd64.deb"; \
        export opencl="https://github.com/intel/compute-runtime/releases/download/19.41.14441/intel-opencl_19.41.14441_amd64.deb"; \
        export ocloc="https://github.com/intel/compute-runtime/releases/download/19.41.14441/intel-ocloc_19.41.14441_amd64.deb"; \
    else export LIBBOOST="libboost-filesystem1.58.0 libboost-thread1.58.0"; \
        export OV_APT="intel-openvino-dev-ubuntu16-${OV_VERSION}"; \
        export gmmlib="https://github.com/intel/compute-runtime/releases/download/19.04.12237/intel-gmmlib_18.4.1_amd64.deb"; \
        export igc_core="https://github.com/intel/compute-runtime/releases/download/19.04.12237/intel-igc-core_18.50.1270_amd64.deb"; \
        export igc_opencl="https://github.com/intel/compute-runtime/releases/download/19.04.12237/intel-igc-opencl_18.50.1270_amd64.deb"; \
        export ocloc="https://github.com/intel/compute-runtime/releases/download/19.04.12237/intel-ocloc_19.04.12237_amd64.deb"; \
        export opencl="https://github.com/intel/compute-runtime/releases/download/19.04.12237/intel-opencl_19.04.12237_amd64.deb"; \
    fi && \
    apt update && \
    apt -y install apt-transport-https ca-certificates python3.5 python3-pip zip x11-apps lsb-core wget cpio sudo $LIBBOOST libboost-python-dev libpng-dev zlib1g-dev git libnuma1 ocl-icd-libopencl1 clinfo protobuf-compiler libprotoc-dev autoconf automake libtool libjson-c-dev && \
    rm -rf /var/lib/apt/lists/* && \
    locale-gen en_US.UTF-8 && update-locale LANG=en_US.UTF-8 && \
    pip3 install cython numpy==1.18.4 && \
# Install CMake
    mkdir -p /opt/cmake/bin && \
    cd ${MY_ROOT} && \
    wget https://github.com/Kitware/CMake/releases/download/v3.13.2/cmake-3.13.2-Linux-x86_64.tar.gz && \
    tar -xf cmake-3.13.2-Linux-x86_64.tar.gz --strip 1 -C /opt/cmake && rm -rf ${MY_ROOT}/cmake-3.13.2-Linux-x86_64.tar.gz && \
# Install openvino using APT repository
    wget https://apt.repos.intel.com/openvino/2020/GPG-PUB-KEY-INTEL-OPENVINO-2020 && \
    apt-key add GPG-PUB-KEY-INTEL-OPENVINO-2020 && \
    cd /etc/apt/sources.list.d && \
    echo "deb https://apt.repos.intel.com/openvino/2020 all main">intel-openvino-2020.list && \ 
    apt update && \
    apt -y install $OV_APT.? && \
    cd ${INTEL_OPENVINO_DIR}/install_dependencies && ./install_openvino_dependencies.sh && \
# Install GPU runtime and drivers
    cd ${MY_ROOT} && \
    mkdir /tmp/opencl && \
    cd /tmp/opencl && \
    wget $gmmlib $igc_core $igc_opencl $opencl $ocloc && \
    dpkg -i /tmp/opencl/*.deb && \
    ldconfig && \
    rm -rf /tmp/opencl && \
# Build onnxruntime
    cd ${MY_ROOT} && \
    git clone --recursive -b $ONNXRUNTIME_BRANCH $ONNXRUNTIME_REPO && \
    sed -i "/pip/d" onnxruntime/dockerfiles/scripts/install_common_deps.sh && \
    /bin/sh onnxruntime/dockerfiles/scripts/install_common_deps.sh && \
    cd onnxruntime/cmake/external/onnx && python3 setup.py install && \
    cd ${MY_ROOT}/onnxruntime && ./build.sh --config Release --update --build --parallel --use_openvino $DEVICE --build_wheel --use_full_protobuf && \
    pip3 install build/Linux/Release/dist/*-linux_x86_64.whl && \
    cd ${MY_ROOT}/ && rm -rf cmake-3.14.3-Linux-x86_64 onnxruntime && \
    cd ${INTEL_OPENVINO_DIR}/ && rm -rf documentation && cd deployment_tools/ && rm -rf model_optimizer open_model_zoo demo && cd inference_engine && rm -rf samples