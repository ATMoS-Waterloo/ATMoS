FROM mg-gw-base

# Configure start-up script
RUN apt install -y screen
COPY *.sh /root/
CMD ["/bin/bash", "/root/entry.sh"]


