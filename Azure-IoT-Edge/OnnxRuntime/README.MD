# Quick-start Docker containers for ONNX Runtime OpenVino EP

This folder has three Docker files:
```
    Dockerfile.openvino : This docker file is used to build openvino base image
    Dockerfile : This docker file is used to build onnxrt with Openvino Execution Provider. Takes in openvino as base image
    Dockerfile.iot : This is used for building docker images which can deployed through Azure IotEdge
```
1. Build base openVINO docker image as follows:

   Download OpenVINO online installer version 2019 R3.1 from [here](https://software.intel.com/en-us/openvino-toolkit/choose-download) and copy the openvino tar file in the same directory as the Dockerfile.openvino and build the base openvino image. The online installer size is only 16MB and the components needed for the accelerators are mentioned in the dockerfile. 
     ```
     # This docker image has all the openvino dependencies along with CPU, GPU and VAD-M drivers. This will be base image with name openvino
      docker build -t openvino -f Dockerfile.openvino --network host .
     ```
      
2. Build and run ONNXRT with Openvino EP on different hardware/accelarator as below:  

    Use the 'Dockerfile' to build the onnxrt with openvino EP. This dockerfile has openvino as base image. You can pass build arguments while building docker image by specifying  --build-arg DEVICE=CPU_FP32  or --build-arg ONNXRUNTIME_REPO=https://github.com/intel/onnxruntime or --build-arg ONNXRUNTIME_BRANCH=master
    Providing the argument device enables onnxruntime to build for a particular device. You can also provide arguments ONNXRUNTIME_REPO and ONNXRUNTIME_BRANCH to test a particular repo and branch. Default is https://github.com/intel/onnxruntime for repo and master for branch. Please change it accordingly while building the image.
    
      ### CPU Version 

      1. Build CPU onnxruntime docker image: 

          ```
          docker build -t onnxruntime-cpu -f Dockerfile --build-arg DEVICE=CPU_FP32 --network host .
          ```
      2. Run the docker image
          ```
          docker run -it onnxruntime-cpu
          ```

      ### GPU Version

      1. Build GPU onnxruntime docker image:

          ``` 
          docker build -t onnxruntime-gpu -f Dockerfile --build-arg DEVICE=GPU_FP32 --network host . 
          ```
        
      2. Run the docker image
          ```
          docker run -it --device /dev/dri:/dev/dri onnxruntime-gpu:latest
          ```
     ### Myriad VPU Accelerator Version 

     1. Build onnxruntime Myriad image from the DockerFile in this repository.
        ``` 
         docker build -t onnxruntime-myriad -f Dockerfile --build-arg DEVICE=MYRIAD_FP16 --network host . 
        ```
     2. Install the Myriad rules drivers on the host machine according to the reference in [here](https://docs.openvinotoolkit.org/latest/_docs_install_guides_installing_openvino_linux.html#additional-NCS-steps)
     3. Run the docker image by mounting the device drivers
        ```
        docker run -it --network host --privileged -v /dev:/dev  onnxruntime-myriad:latest

        ```
      ### VAD-M Accelerator Version 

      1. Build VAD-M onnxruntime docker image: 
      
         Build the docker image from the DockerFile in this repository.
         ``` 
         docker build -t onnxruntime-vadm -f Dockerfile --build-arg DEVICE=VAD-M_FP16 --network host . 
         ```
   
      2. Install the HDDL drivers on the host machine according to the reference in [here](https://docs.openvinotoolkit.org/latest/_docs_install_guides_installing_openvino_linux_ivad_vpu.html)
      3. Run the docker image by mounting the device drivers
         ```
         docker run -it --device --mount type=bind,source=/var/tmp,destination=/var/tmp --device /dev/ion:/dev/ion  onnxruntime-hddl:latest
         ```

## Deploy ONNX Runtime-OpenvinoEP modules through Azure Iot Edge 
1 Deploy these images by following the tutorial in here [Azure IOT Edge](https://docs.microsoft.com/en-us/azure/iot-edge/quickstart-linux). We have the sample docker file Dockerfile.iot. The base image can be onnxruntime-cpu/gpu/vadm based on the accelerator selected. Please edit the Docker file to change base image name that was built for the accelerator.

   - Build the docker image based on DockerFile.iot in this repository.
     ``` 
      docker build -t onnx-iot -f Dockerfile.iot --build-arg MODEL_XML_PATH=<onnxmodel> --build-arg INPUT=<inputimage> --build-arg SCRIPTNAME=<scriptname> --network host . 
     ```
     One can pass arguments like the onnx model file(MODEL_XML_PATH), inference script(SCRIPTNAME) and input image name(INPUT) as build arguments while building the docker image or while deploying the image via Azure console in the environment variables section. 
    
2. Provide the below configuration details while deploying the iot module on Azure portal. 

    -- For environment variables in Azure deployment page
    
	|Environment Variables | Value |
	| --------- | -------- |
	| <code>MODEL_XML_PATH</code> | specify path to onnx model|
	| <code>CONNECTIONSTRING</code> |Azure Iot Hub connection string |
	| <code>SCRIPTNAME</code> | specify path to inference script |
	| <code>INPUT</code> | specify path to input image for inference |
	

   - In the Container Create Options section please use below config details
      ```
      <DATA> : is the path on the edge system where the input artifacts are located
       ```
      For CPU,
      ```
      {
       "HostConfig": {
	    "Binds": [
             	"<DATA>:<DATA>"
	      ]
	   }
	 }
       ```
   
      For GPU,
  
      ```
      {
       "HostConfig": {
	    "Binds": [
             	"<DATA>:<DATA>"
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
     FOR VAD-M,
  
      ```
      {
       "HostConfig": {
	    "Binds": [
		"/var/tmp:/var/tmp",
                "<DATA>:<DATA>"
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
      For Myriad,
      
       ```
       {
              "HostConfig":
              {
                             "Binds":
                             [
                                           "/dev:/dev"
                             ],
                             "NetworkMode":"host",
                             "IpcMode":"host",
                             "Privileged":true
              },
              "NetworkingConfig":
              {
                             "EndpointsConfig":
                             {
                                           "host":
                                           {}
                             }
              }
       }
      ```
       
     
  ### ONNX Models
  Pre trained ONNX Models for evaluation can be downloaded from the [ONNX Model Zoo](https://github.com/onnx/models).


