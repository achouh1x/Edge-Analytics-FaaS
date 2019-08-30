# Quick-start Docker containers for ONNX Runtime OpenVino EP

0. Prerequisites: Build openvino image with OpenVINO version 2019 R1.1. 
   
1. Retrieve your base openVINO docker image as follows:

    Build the openVINO docker image from the DockerFile in this repository. Before that, download OpenVINO online installer version 2019 R1.1 from [here](https://software.intel.com/en-us/openvino-toolkit/choose-download) and copy the openvino tar file in the same directory and build the image. The online installer size is only 16MB and the components needed for the accelerators are mentioned in the dockerfile. 
     ```
     # This docker image has all the openvino dependencies along with CPU, GPU and VAD-R drivers. This will be base image with name openvino
      docker build -t openvino -f Dockerfile.openvino --network host .
     ```
      
2. Steps to build and run on different hardware/accelarator are provided below:  

    Providing the argument device enables onnxruntime for that particular device. You can also provide arguments ONNXRUNTIME_REPO and ONNXRUNTIME_BRANCH to test a particular repo and branch. Default is https://github.com/intel/onnxruntime for repo and master for branch. Please change it accordingly while building the image.
      ### CPU Version 

      1. Build your docker image: 

         Build the docker image from the DockerFile in this repository. 
        
          ```
          docker build -t onnxruntime-cpu --build-arg DEVICE=CPU_FP32 --network host .
          ```
      2. Run the docker image
          ```
          docker run -it onnxruntime-cpu
          ```

      ### GPU Version

      1. Build your docker image:

         Build the docker image from the DockerFile in this repository.
          ``` 
          docker build -t onnxruntime-gpu --build-arg DEVICE=GPU_FP32 --network host . 
          ```
        
      2. Run the docker image
          ```
          docker run -it --device /dev/dri:/dev/dri onnxruntime-gpu:latest
          ```
     ### Myriad VPU Accelerator Version 

     1. Build the docker image from the DockerFile in this repository.
        ``` 
         docker build -t onnxruntime-myriad --build-arg DEVICE=MYRIAD_FP16 --network host . 
        ```
     2. Install the Myriad rules drivers on the host machine according to the reference in [here](https://docs.openvinotoolkit.org/latest/_docs_install_guides_installing_openvino_linux.html#additional-NCS-steps)
     3. Run the docker image by mounting the device drivers
        ```
        docker run -it --network host --privileged -v /dev:/dev  onnxruntime-myriad:latest

        ```
      ### VAD-R Accelerator Version 

      1. Build your docker image: 
      
         Build the docker image from the DockerFile in this repository.
         ``` 
         docker build -t onnxruntime-vadr --build-arg DEVICE=VAD-R_FP16 --network host . 
         ```
   
      2. Install the HDDL drivers on the host machine according to the reference in [here](https://docs.openvinotoolkit.org/latest/_docs_install_guides_installing_openvino_linux_ivad_vpu.html)
      3. Run the docker image by mounting the device drivers
         ```
         docker run -it --device --mount type=bind,source=/var/tmp,destination=/var/tmp --device /dev/ion:/dev/ion  onnxruntime-hddl:latest
         ```

## Azure IOt Edge with ONNX Runtime-OpenvinoEP

1 Deploy these image through [Azure IOT Edge](https://docs.microsoft.com/en-us/azure/iot-edge/quickstart-linux) with the docker file Dockerfile.iot. The base image can be onnxruntime-cpu/gpu/vadr based on the accelerator selected. Please edit the Docker file to change base image name that was built for the accelerator.

   - Build the docker image from the DockerFile in this repository.
     ``` 
      docker build -t onnx-iot -f Dockerfile.iot --build-arg MODEL_XML_PATH=<onnxmodel> --build-arg INPUT=<inputimage> --build-arg SCRIPTNAME=<scriptname> --build-arg CONNECTIONSTRING=<iotedgeconnectionstring> --network host . 
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


