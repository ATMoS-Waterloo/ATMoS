FROM mg-host-base

USER root

RUN apt-get install -y iptables tmux screen net-tools iputils-ping tcpdump git hping3 python-pip

WORKDIR /root/

COPY *.sh /root/

ENTRYPOINT []
CMD ["/bin/bash", "/root/entry.sh"]

#ENTRYPOINT ["/bin/bash"]
