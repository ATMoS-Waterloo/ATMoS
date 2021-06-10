FROM bkimminich/juice-shop

USER root

#RUN cat /etc/os-release

RUN apk add bash iptables tmux screen net-tools iputils tcpdump git hping3 wget curl --update-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing

COPY *.sh /root/

ENTRYPOINT []

CMD ["/bin/bash", "/root/entry.sh"]

