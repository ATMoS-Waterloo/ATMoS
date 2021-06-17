#!/bin/bash

DIR=$(dirname $0)

#until ifconfig $(cat /etc/hostname)-eth0
#do
#  sleep 1
#end

# add route
route add default gw $(ifconfig $(cat /etc/hostname)-eth0 | grep -oE "inet addr:([0-9].?)+" | grep -oE "([0-9]+\.)+")200
route del default gw $(ifconfig eth0 | grep -oE "inet addr:([0-9].?)+" | grep -oE "([0-9]+\.)+")1

(
while [ true ]
do
  curl -o /dev/null -L http://google.com
  curl -o /dev/null -L http://google.com
  sleep 1
  curl -o /dev/null -L http://google.com
  sleep 5
done
) &

/main.sh
