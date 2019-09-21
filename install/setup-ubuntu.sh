#!/bin/bash

BASE_DIR=/root

cd $BASE_DIR

apt install -y openjdk-8-java

apt install -y git

git clone https://github.com/blackvvine/gemel-sdn.git

# install ODL
apt-add-repository ppa:ansible/ansible -y
apt-get update
apt-get install -y ansible
ansible-playbook gemel-sdn/provision/scripts/odl.yml

# install gemel-net
git clone https://github.com/blackvvine/gemelnet
ln -s containernet gemelnet
cd gemelnet/ansible
ansible-playbook -i "localhost," -c local install.yml
cd ../..

# add gemel-sdn to python path
echo "export PYTHONPATH=\"\$PYTHONPATH:$(realpath $BASE_DIR)/gemel-sdn\"" >> ~/.bashrc
echo "export PYTHONPATH=\"\$PYTHONPATH:$(realpath $BASE_DIR)/bella-agent\"" >> ~/.bashrc
echo "export PYTHONPATH=\"\$PYTHONPATH:$(realpath $BASE_DIR)/gemelnet\"" >> ~/.bashrc

# install anaconda
# wget https://repo.anaconda.com/archive/Anaconda3-2019.07-Linux-x86_64.sh
# pip install jupyter tensorflow

# clone bella
git clone https://github.com/simorgh-project/bella-agent.git

# add fake URLs
# echo "127.0.0.1	odl.einstein.eeman.me" >> /etc/hosts
# echo "127.0.0.1	halsey.einstein.eeman.me" >> /etc/hosts

sudo add-apt-repository ppa:jonathonf/python-3.6
apt update
apt-get install -y python3.6 python-pip
virtualenv -p /usr/bin/python3.6 jupenv
. jupenv/bin/activate
pip install tensorflow jupyter

/usr/local/vtn/bin/vtn_stop
/usr/local/vtn/bin/vtn_start
/usr/local/vtn/sbin/unc_dmctl status





