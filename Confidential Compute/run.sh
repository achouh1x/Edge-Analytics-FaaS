#!/bin/bash
GRAPHENE_INSTALL_DIR=$1

usage() { 
	echo -e "\nUsage:\n./run.sh [graphene install dir] \n"
	exit 1
	} 

if [ "$1" == "" ]
then
	echo "Enter Graphene Install Directory"
	usage
fi

if [ ! -f  $GRAPHENE_INSTALL_DIR/Pal/src/host/Linux-SGX/signer/enclave-key.pem ]; then
    openssl genrsa -3 -out $GRAPHENE_INSTALL_DIR/Pal/src/host/Linux-SGX/signer/enclave-key.pem 3072
fi

# Build SVM Docker image
echo "--------------------------------------------------------------"
echo "Building SVM Docker image"
echo "--------------------------------------------------------------"
docker build . --build-arg GRAPHENE_INSTALL_DIR=$GRAPHENE_INSTALL_DIR -t svm:latest

echo "--------------------------------------------------------------"
echo "Running SVM Application with Graphene-SGX "
echo "--------------------------------------------------------------"

CURRENT_DIR=$PWD
cd $GRAPHENE_INSTALL_DIR/Tools

#Copy application manifest
cp $CURRENT_DIR/gen_manifest $GRAPHENE_INSTALL_DIR/Tools

#Apply gsce workaround
git checkout gsce 
git apply $CURRENT_DIR/gsce_fix.patch

#Run SVM App with graphene sgx
./gsce run svm:latest

#Deleting the enclave signing key for security reasons.
rm -f  $GRAPHENE_INSTALL_DIR/Pal/src/host/Linux-SGX/signer/enclave-key.pem 
