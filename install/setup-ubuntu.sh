#!/bin/bash

# get current script dir
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# install destination dir
BASE_DIR=/root

cd $BASE_DIR

apt install -y openjdk-8-jdk
apt install -y git

# install Python 3.7
add-apt-repository ppa:deadsnakes/ppa
apt update
apt install -y python3.7 python3.7-gdbm
# update-alternatives --install /usr/bin/python python /usr/bin/python3.7 2
# update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 2
apt install -y python3-pip

# install ODL
apt-add-repository --yes --update ppa:ansible/ansible
apt update
apt install -y ansible
ansible-playbook $DIR/odl.yml

# install gemel-net (from abagarre repo)
git clone https://github.com/abagarre/gemelnet
ln -s gemelnet containernet
cd gemelnet/ansible
ansible-playbook -i "localhost," -c local install.yml
cd ../..

# add gemel-sdn to python path
echo "export PYTHONPATH=\"\$PYTHONPATH:$(realpath $DIR/../lib)\"" >> ~/.bashrc
echo "export PYTHONPATH=\"\$PYTHONPATH:$(realpath $BASE_DIR)/gemelnet\"" >> ~/.bashrc

# install environment for Jupyter and Machine Learning
pip3 install virtualenv
virtualenv -p /usr/bin/python3.7 jupenv
. jupenv/bin/activate
pip3 install tensorflow jupyter

# start ODL
/usr/local/vtn/bin/vtn_stop
/usr/local/vtn/bin/vtn_start
/usr/local/vtn/bin/unc_dmctl status





