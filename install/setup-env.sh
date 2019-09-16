#!/bin/bash


DIR=$(dirname $0)
BASE_DIR="$DIR"

cd $BASE_DIR

# install python3.6
sudo add-apt-repository -y ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install -y python3.6 python3-pip

# install docker
sudo apt-get install -y docker.io

# clone Gemel SDN python API
git clone git@github.com:blackvvine/gemel-sdn.git
echo "export PYTHONPATH=\"\$PYTHONPATH:$(realpath $BASE_DIR)/gemel-sdn\"" >> ~/.bashrc

# install Docker and build containers
git clone git@github.com:blackvvine/mini-gemel.git
cd mini-gemel/images
make
cd ..

# install gemelnet
git clone git@github.com:blackvvine/gemelnet.git
echo "export PYTHONPATH=\"\$PYTHONPATH:$(realpath $BASE_DIR)/gemelnet\"" >> ~/.bashrc
ln -s $BASE_DIR/gemelnet/mininet $BASE_DIR/mini-gemel/topo/


