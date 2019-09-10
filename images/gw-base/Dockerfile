FROM mg-base

WORKDIR /root

COPY snort-2.9.9.0.tar.gz /root/
COPY daq-2.0.6.tar.gz /root/

RUN apt install -y gcc 
RUN apt install -y build-essential 
RUN apt install -y pkg-config 
RUN apt install -y make 
RUN apt install -y g++ 
RUN apt install -y libpcap-dev tcpdump libpcre3-dev libdnet-dev
RUN apt install -y libdumbnet-dev
RUN apt install -y cmake

# Extract source files
RUN tar -xvzf snort-2.9.9.0.tar.gz
RUN tar -xvzf daq-2.0.6.tar.gz

# Install DAQ
WORKDIR /root/daq-2.0.6
RUN apt install -y bison flex
RUN apt install -y zlib1g-dev
RUN ./configure
RUN make
RUN sudo make install

# Install Snort
WORKDIR /root/snort-2.9.9.0
RUN ./configure --enable-sourcefire
RUN make
RUN sudo make install
RUN ldconfig

WORKDIR /root

# Install dependencies for Barnyard & Snort configs
RUN apt install -y software-properties-common
RUN apt-add-repository ppa:ansible/ansible -y
RUN apt update -y
RUN apt install -y ansible
RUN apt install -y mysql-server
RUN apt install -y mysql-client
RUN apt install -y libmysqlclient-dev
RUN apt install -y autoconf
RUN apt install -y libtool

# Basic Snort and Barnyard configs
COPY snort.yml /root/
RUN ansible-playbook /root/snort.yml

# Add local rules
COPY etc/snort/rules/local.rules /etc/snort/rules/

# Init Barnyard database
COPY queries.sh /root/
RUN /root/queries.sh

