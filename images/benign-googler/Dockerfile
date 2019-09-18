FROM  iman/puppet-master:1 

COPY entry.sh /usr/src/app/

USER root

RUN apt-get install -y iptables tmux screen net-tools iputils-ping tcpdump

# CMD bash src/dispatch.sh google benign
CMD ["/bin/bash", "/usr/src/app/entry.sh"]



