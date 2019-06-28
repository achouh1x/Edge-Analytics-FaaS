#!/bin/bash

# Installing SGX SDK
echo "--------------------------------------------------------------"
echo "Installing pre-requisites"
echo "--------------------------------------------------------------"
sudo apt-get install -y git build-essential ocaml automake autoconf libtool wget python libssl-dev
#PSW
sudo apt-get install -y libssl-dev libcurl4-openssl-dev protobuf-compiler libprotobuf-dev debhelper cmake
sudo apt-get install -y libssl-dev libcurl4-openssl-dev libprotobuf-dev
sudo apt install -y python-pip
sudo apt install -y build-essential
sudo apt install -y autoconf
sudo apt install -y gawk
sudo apt install -y gcc
sudo apt install -y python-protobuf
echo "--------------------------------------------------------------"
echo "Installing Docker-CE!"
echo "--------------------------------------------------------------"
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
sudo groupadd docker
sudo gpasswd -a $USER docker
sudo apt-get install -y docker-ce
sudo docker run hello-world
echo "--------------------------------------------------------------"
echo "Installing Docker-CE Completed!"
echo "--------------------------------------------------------------"
sudo rm -rf "$HOME/sgx-packsge"
mkdir -p "$HOME/sgx-package"
cd $HOME/sgx-package
echo "--------------------------------------------------------------"
echo "Installing SGX Driver!"
echo "--------------------------------------------------------------"
git clone https://github.com/intel/linux-sgx-driver.git
cd $HOME/sgx-package/linux-sgx-driver/
git checkout tags/sgx_driver_1.9
dpkg-query -s linux-headers-$(uname -r)
sudo apt-get install -y linux-headers-$(uname -r)
make -j99
sudo mkdir -p "/lib/modules/"`uname -r`"/kernel/drivers/intel/sgx"    
sudo cp isgx.ko "/lib/modules/"`uname -r`"/kernel/drivers/intel/sgx"    
sudo sh -c "cat /etc/modules | grep -Fxq isgx || echo isgx >> /etc/modules"    
sudo /sbin/depmod
sudo /sbin/modprobe isgx
temp_file=$(mktemp)
echo $HOME/sgx-package/linux-sgx-driver > ${temp_file}
echo "1.9" >> ${temp_file}
echo "" >> ${temp_file}
echo "--------------------------------------------------------------"
echo "Completed SGX Driver Installation"
echo "--------------------------------------------------------------"
echo "--------------------------------------------------------------"
echo "Installing SGX SDK!"
echo "--------------------------------------------------------------"
cd $HOME/sgx-package
git clone https://github.com/intel/linux-sgx.git
cd $HOME/sgx-package/linux-sgx
./download_prebuilt.sh
make -j99
make -j99 sdk_install_pkg
make deb_pkg
sudo apt-get install -y build-essential python
cd $HOME/sgx-package/linux-sgx/linux/installer/bin/
yes yes | ./sgx_linux_x64_sdk_2.5.101.50123.bin 
source $HOME/sgx-package/linux-sgx/linux/installer/bin/sgxsdk/environment 
cd $HOME/sgx-package/linux-sgx/SampleCode/LocalAttestation
make -j99
cd $HOME/sgx-package/linux-sgx/SampleCode/LocalAttestation
yes m | ./app
cd $HOME/sgx-package/linux-sgx/linux/installer/deb/
sudo dpkg -i ./libsgx-urts_2.5.101.50123-xenial1_amd64.deb ./libsgx-enclave-common_2.5.101.50123-xenial1_amd64.deb
echo "--------------------------------------------------------------"
echo "Completed Installation of SGX SDK and PSW SDK"
echo "--------------------------------------------------------------"
echo "--------------------------------------------------------------"
echo "Installing Graphene SDK"
echo "--------------------------------------------------------------"
cd $HOME/sgx-package
git clone https://github.com/oscarlab/graphene.git
cd $HOME/sgx-package/graphene
git checkout v0.6-209-g87b1937
git submodule update --init
sed -i '/from Crypto.PublicKey import RSA/d' $HOME/sgx-package/graphene/Pal/src/host/Linux-SGX/signer/pal-sgx-get-token
make -j99
cd $HOME/sgx-package/graphene/Pal/src/host/Linux-SGX/signer
cd $HOME/sgx-package/graphene/Pal/src
make -j99 SGX=1 <${temp_file}
cd $HOME/sgx-package/graphene/Pal/src/host/Linux-SGX/sgx-driver
make -j99
sudo ./load.sh
cd $HOME/sgx-package/graphene/LibOS
make -j99
cd $HOME/sgx-package/graphene/LibOS/shim/test/native
make -j99 SGX=1
make -j99 SGX_RUN=1
sudo sysctl vm.mmap_min_addr=0
./pal_loader SGX helloworld
SGX=1 ./pal_loader helloworld 
cd $HOME/sgx-package/graphene/LibOS/shim/test/apps/python
make -j99 SGX=1
make -j99 SGX_RUN=1
SGX=1 ./python.manifest.sgx scripts/helloworld.py
[ -e ${temp_file} ] && rm -f ${temp_file} 
echo "--------------------------------------------------------------"
echo "Completed installation of Graphene SDK"
echo "--------------------------------------------------------------"

