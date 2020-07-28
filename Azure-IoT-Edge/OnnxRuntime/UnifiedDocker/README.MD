# Quick-start Docker containers for ONNX Runtime
1. Build the onnxruntime image for all the accelerators supported as below 

   Retrieve your docker image in one of the following ways.

    -  For building the docker image, provide the argument DEVICE which enables onnxruntime for that particular device. For FPGA, you can specify the dockerfile.fpga with -f tag and no need to pass the DEVICE argument. You can also provide arguments ONNXRUNTIME_REPO, ONNXRUNTIME_BRANCH to test that particular repo and branch and also UBUNTU_VERSION and OV_VERSION. Default is https://github.com/microsoft/onnxruntime for repo, master for branch, 16.04 for ubuntu version and 2020.3.194 for ov version, can build for ubuntu version 18.04 and ov version 2020.4.287 also.
       ```
       docker build -t onnxruntime --build-arg DEVICE=$DEVICE .
       ``` 
    -  Pull the official image from DockerHub.
       ```
     	# Will be available with next release
       ```   

2. DEVICE: Specifies the hardware target for building OpenVINO Execution Provider. Below are the options for different Intel target devices.

	| Device Option | Target Device |
	| --------- | -------- |
	| <code>CPU_FP32</code> | Intel<sup></sup> CPUs |
	| <code>GPU_FP32</code> |Intel<sup></sup> Integrated Graphics |
	| <code>GPU_FP16</code> | Intel<sup></sup> Integrated Graphics |
	| <code>MYRIAD_FP16</code> | Intel<sup></sup> Movidius<sup>TM</sup> USB sticks |
	| <code>VAD-M_FP16</code> | Intel<sup></sup> Vision Accelerator Design based on Movidius<sup>TM</sup> MyriadX VPUs |
  Note: Since there is a specific dockerfile for FPGA, no need to pass VAD-F_FP32 as DEVICE. 
## CPU Version 

1. Retrieve your docker image in one of the following ways.

   -Build the docker image from the DockerFile in this repository. 
     
     ```
     docker build -t onnxruntime-cpu --build-arg DEVICE=CPU_FP32 --network host .
     ```
   - Pull the official image from DockerHub.
     ```
     # Will be available with next release
     ```
2. Run the docker image
    ```
     docker run -it onnxruntime-cpu
    ```

## GPU Version

1. Retrieve your docker image in one of the following ways. 
   - Build the docker image from the DockerFile in this repository.
     ``` 
      docker build -t onnxruntime-gpu --build-arg DEVICE=GPU_FP32 --network host . 
     ```
   - Pull the official image from DockerHub.
     ```
       # Will be available with next release
     ```

2. Run the docker image
    ```
    docker run -it --device /dev/dri:/dev/dri onnxruntime-gpu:latest
    ```
## Myriad VPU Accelerator Version 

1. Retrieve your docker image in one of the following ways. 
   - Build the docker image from the DockerFile in this repository.
     ``` 
      docker build -t onnxruntime-myriad --build-arg DEVICE=MYRIAD_FP16 --network host . 
     ```
   - Pull the official image from DockerHub.
     ```
      # Will be available soon
     ```
2. Install the Myriad rules drivers on the host machine according to the reference in [here](https://docs.openvinotoolkit.org/latest/_docs_install_guides_installing_openvino_linux.html#additional-NCS-steps)
3. Run the docker image by mounting the device drivers
    ```
    docker run -it --network host --privileged -v /dev:/dev  onnxruntime-myriad:latest
    ```
## VAD-M Accelerator Version 

1. Retrieve your docker image in one of the following ways. 
   - Build the docker image from the DockerFile in this repository.
     ``` 
      docker build -t onnxruntime-vadm --build-arg DEVICE=VAD-M_FP16 --network host . 
     ```
   - Pull the official image from DockerHub.
     ```
      # Will be available soon
     ```
2. Install the drivers on the host machine according to the reference in [here](https://docs.openvinotoolkit.org/latest/_docs_install_guides_installing_openvino_linux_ivad_vpu.html)
3. Run the docker image by mounting the device drivers
    ```
    docker run -it --mount type=bind,source=/var/tmp,destination=/var/tmp --device /dev/ion:/dev/ion  onnxruntime-vadm:latest
    ```

## FPGA Accelerator Version 
1. Download OpenVINO version 2020.3 for Linux targets with FPGA support from [here](https://software.intel.com/content/www/us/en/develop/tools/openvino-toolkit.html) and copy the openvino tar file in the same directory of dockerfile.fpga. The online installer size is only 19MB and the components needed for the accelerator are mentioned in the dockerfile.
2. Setup FPGA on host machine. Refer [here](https://docs.openvinotoolkit.org/2020.3/_docs_install_guides_VisionAcceleratorFPGA_Configure.html) for details.
3. To test if FPGA card was installed succesfully run aocl diagnose:
    ```
    aocl diagnose
    ```
   You should see DIAGNOSTIC_PASSED before proceeding to the next steps.
4. Retrieve your docker image in one of the following ways. 
   - Build the docker image from the DockerFile.fpga in this repository.
     ``` 
      docker build -t onnxruntime-fpga -f Dockerfile.fpga --network host .  
     ```
   - Pull the official image from DockerHub.
     ```
      # Will be available soon
     ```

5. Run the docker image (Update the command with your kernal version. Tested successfully for 4.15.0-96-generic and and 4.15.0-99-generic)
    ```
    docker run --rm -it --net=host --privileged --mount type=bind,source=/opt/altera,destination=/opt/altera --mount type=bind,source=/opt/Intel/OpenCL/Boards,destination=/opt/Intel/OpenCL/Boards --mount type=bind,source=/usr/src/kernels/4.15.0-96-generic/,destination=/usr/src/linux-headers-4.15.0-96-generic --mount type=bind,source=/opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/,destination=/opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/ -v /opt/intel/openvino/bitstreams/:/opt/intel/openvino/bitstreams/ -v /etc/udev/:/etc/udev/ --device /dev/:/dev/ onnxruntime-fpga:latest
    ```

## Choose hardware target dynamically
The target hardware selected during Docker build stage forms the Default hardware target. This value however can be overriden with a different target at runtime by calling the corresponding APIs from the application. Refer to this [Dynamic device selection API documentation](https://github.com/intel/onnxruntime/blob/openvino-ep-v2/docs/execution_providers/OpenVINO-ExecutionProvider.md#dynamic-device-selection) for more details.

## Minify Docker Containers
You can minify and secure your docker containers using docker-slim. It is free and open source. Docker slim will analyse your image, understands what it needs and remove all others. Also you can set flags like `--include-path` to make sure everything your application needs is included. Refer [docker-slim](https://github.com/docker-slim/docker-slim) for more details.

## Azure IOt Edge with ONNX Runtime-OpenvinoEP

1 Deploy these image through Azure IOT Edge with the docker file Dockerfile.iot. The base image can be onnxruntime-cpu/gpu/vadm based on the accelerator selected. Please edit the Docker file to change base image name that was built for the accelerator.

   - Build the docker image from the DockerFile in this repository.
     ``` 
      docker build -t onnx-iot --network host .
     ```
2. Provide the below configuration details while deploying the iot module on Azure portal. 

	|Environment Variables | Value |
	| --------- | -------- |
	| <code>MODEL_XML_PATH</code> | /opt/intel/dl/data/model.onnx |
	| <code>CONNECTIONSTRING</code> |azure iothub connection string |
	| <code>SCRIPTNAME</code> | /opt/intel/dl/data/pythonscrit_name |
	| <code>INPUT</code> | /opt/intel/data/imagename |
	

   - In the Container Create Options please replace as below

     FOR VAD-M,
  
      ```
      {
       "HostConfig": {
	    "Binds": [
		"/var/tmp:/var/tmp",
                "/opt/intel/dl/data:/opt/intel/dl/data"
	      ],
	    "Devices": [
	      {
			"PathOnHost": "/dev/ion",
			"PathInContainer": "/dev/ion",
			"CgroupPermissions": "rwm"
	      }
	    ]
	   }
	 }
       ```
      FOR GPU,
  
      ```
      {
       "HostConfig": {
	    "Binds": [
             	"/opt/intel/dl/data:/opt/intel/dl/data"
	      ],
	    "Devices": [
	      {
			"PathOnHost": "/dev/dri",
			"PathInContainer": "/dev/dri",
			"CgroupPermissions": "rwm"
	      }
	    ]
	   }
	 }
       ```
