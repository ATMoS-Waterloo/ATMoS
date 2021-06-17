FROM hightechsec/docker-dvwa

#RUN cat /etc/os-release
RUN apt-get update && \
    apt-get -y install curl net-tools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY *.sh /root/

ENTRYPOINT []

CMD ["/bin/bash", "/root/entry.sh"]

