# Quick-start Docker containers for ONNX Runtime OpenVino EP

0. Prerequisites: Build openvino image with OpenVINO version 2018 R5.0.1.
   
1. Retrieve your docker image in one of the following ways.

   - Build the docker image from the DockerFile in this repository. Before that, download and copy the openvino tar file in the directory  and build the image
     ```
      # This docker image has all the openvino dependencies along with CPU, GPU and VAD-R drivers. This will be base image with name openvino
      docker build -t openvino -f Dockerfile.openvino .
     ```
   - Pull the official image from DockerHub.
   

2. Build the onnxruntime image for all the accelerators supported as below with openvino as base image
    ```
     docker build -t onnxruntime-$device --build-arg DEVICE=$DEVICE .
    ```
    DEVICE: Specifies the hardware target for building OpenVINO Execution Provider. Below are the options for different Intel target devices.

	| Device Option | Target Device |
	| --------- | -------- |
	| <code>CPU_FP32</code> | Intel<sup>®</sup> CPUs |
	| <code>GPU_FP32</code> |Intel<sup>®</sup> Integrated Graphics |
	| <code>GPU_FP16</code> | Intel<sup>®</sup> Integrated Graphics |
	| <code>MYRIAD_FP16</code> | Intel<sup>®</sup> Movidius<sup>TM</sup> USB sticks |
	| <code>VAD-R_FP16</code> | Intel<sup>®</sup> Vision Accelerator Design based on Movidius<sup>TM</sup> MyriadX VPUs |

## CPU Version 

1. Retrieve your docker image in one of the following ways.

   - Build the docker image from the DockerFile in this repository. Providing the argument device enables onnxruntime for that particular device
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
      docker build -t onnxruntime-gpu --build-arg DEVICE=GPU_FP32 --network host . .
     ```
   - Pull the official image from DockerHub.
     ```
       # Will be available with next release
     ```

2. Run the docker image
    ```
    docker run -it --device /dev/dri:/dev/dri onnxruntime-gpu:latest
    ```

## VAD-R Accelerator Version 

1. Retrieve your docker image in one of the following ways. 
   - Build the docker image from the DockerFile in this repository.
     ``` 
      docker build -t onnxruntime-vadr --build-arg DEVICE=VAD-R_FP16 --network host . .
     ```
   - Pull the official image from DockerHub.
     ```
      # Will be available with ONNX Runtime 0.2.0
     ```
2. Install the HDDL drivers on the host machine according to the reference in [here](https://docs.openvinotoolkit.org/latest/_docs_install_guides_installing_openvino_linux_ivad_vpu.html)
3. Run the docker image by mounting the device drivers
    ```
    docker run -it --device --mount type=bind,source=/var/tmp,destination=/var/tmp --device /dev/ion:/dev/ion  onnxruntime-hddl:latest
    ```

### Azure IOt Edge with ONNX Runtime-OpenvinoEP

1 Deploy these image through [Azure IOT Edge](https://docs.microsoft.com/en-us/azure/iot-edge/quickstart-linux) with the docker file Dockerfile.iot. The base image can be onnxruntime-cpu/gpu/vadr based on the accelerator selected. Please edit the Docker file to change base image name that was built for the accelerator.

   - Build the docker image from the DockerFile in this repository.
     ``` 
      docker build -t onnx-iot --network host . .
     ```
2. Provide the below configuration details while deploying the iot module on Azure portal. 

	|Environment Variables | Value |
	| --------- | -------- |
	| <code>MODEL_XML_PATH</code> | /opt/intel/dl/data/model.onnx |
	| <code>CONNECTIONSTRING</code> |Azure Iot HUb connection string |
	| <code>SCRIPTNAME</code> | /opt/intel/dl/data/pythonscript |
	| <code>INPUT</code> | /opt/intel/data/image |
	

   - In the Container Create Options please replace as below

     FOR HDDL,
  
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
	
  ### ONNX Models
  Pre trained ONNX Models for evaluation can be downloaded from the [ONNX Model Zoo](https://github.com/onnx/models).


