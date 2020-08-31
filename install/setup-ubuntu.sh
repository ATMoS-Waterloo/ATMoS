#!/bin/bash

# get current script dir
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# install destination dir
BASE_DIR=/root

cd $BASE_DIR

apt install -y openjdk-8-jdk
apt install -y git

# install ODL
apt-add-repository --yes --update ppa:ansible/ansible
apt update
apt install -y ansible
ansible-playbook $DIR/odl.yml

# install gemel-net (from abagarre repo)
git clone https://github.com/abagarre/gemelnet
ln -s gemelnet containernet
ansible-playbook -i "localhost," -c local gemelnet/ansible/install.yml
sh containernet/util/install.sh
# If there is an OVS-testcontroller error:
#service openvswitch-testcontroller stop
#update-rc.d openvswitch-testcontroller disable
#sh containernet/util/install.sh
cd containernet
make develop
cd ..

# install Python 3.7
add-apt-repository ppa:deadsnakes/ppa
apt update
apt install -y python3.7
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1

# Make sure `pip3 -V` correspond to python 3.7
pip3 install python-backports.ssl-match-hostname pytest==4.6.4 docker==2.0.2 python-iptables

# Fix pexpect error
apt remove python3-pexpect
pip3 install pexpect
pip3 install --upgrade --force-reinstall setuptools

# Run again containernet install
sh containernet/util/install.sh
cd containernet
make develop
cd ..

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

