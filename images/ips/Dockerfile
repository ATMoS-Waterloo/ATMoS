FROM mg-gw-base

COPY *.sh /root/

# Add DAQ rules
RUN /root/add-daq-rules.sh

# Configure start-up script
CMD ["/bin/bash", "/root/entry.sh"]


