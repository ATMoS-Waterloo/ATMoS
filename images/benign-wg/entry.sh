#!/bin/bash

DIR=$(dirname $0)

#until ifconfig $(cat /etc/hostname)-eth0
#do
#  sleep 1
#end

# add route
route add default gw $(ifconfig $(cat /etc/hostname)-eth0 | grep -oE "inet addr:([0-9].?)+" | grep -oE "([0-9]+\.)+")200
route del default gw $(ifconfig eth0 | grep -oE "inet addr:([0-9].?)+" | grep -oE "([0-9]+\.)+")1

iptables -t nat -I PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 3000

(
while [ true ]
do
  curl -L http://google.com
  curl -L http://google.com
  sleep 1
  curl -L http://google.com
  sleep 5
done
) &

cd /juice-shop
docker-entrypoint.sh npm start

