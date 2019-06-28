## Runtime protection of ML applications

This project demonstrates runtime protection of [Intel(R) DAAL](https://github.com/intel/daal) based ML sample application using [Graphene-SGX](https://github.com/oscarlab/graphene) within a [Docker](https://github.com/docker/docker-ce) container.<br/>
The Intel(R) DAAL sample used in this case is available here
[svm_two_class_csr_batch.cpp](https://github.com/intel/daal/blob/daal_2019_update3/examples/cpp/source/svm/svm_two_class_csr_batch.cpp)

** Disclaimer: this is a pre-release beta version. Please do no use in production system before further assessment.
---

#### Setup the environment<br/>
* Open a terminal and clone this repository<br/>
* cd to cloned git directory<br/>
* ./setup.sh<br/>
### *Note:*
To run this sample a system with SGX enabled is required, make sure that SGX is enabled in the BIOS before running this setup script.<br/>
The setup script will install the pre-requisites, SGX driver, SGX SDK and Graphene-SGX SDK, Docker-CE etc.<br/>


#### Run SVM sample
* $./run.sh < graphene installation directory > <br/>
   example<br/>
```
   $./run.sh $HOME/sgx-package/graphene
```
The above script builds Docker image svm:latest and 'gsce' graphene script to run the application with graphene-sgx<br/>
### *Note:*<br/>
The version of Graphene-SGX used is v0.6-209-g87b1937
At the time of creating this sample the version of Graphene-SGX used requires SGX driver version 1.9, so the script checks out sgx driver version 1.9<br/>

Report security problems to: https://www.intel.com/content/www/us/en/security-center/default.html
