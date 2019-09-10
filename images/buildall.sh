#!/bin/bash

DIR=$(realpath $(dirname $0))

set -e

echo Build base
cd $DIR/base
./build

echo Build host-base
cd $DIR/host-base
./build

echo Build gateway base
cd $DIR/gw-base
./build

echo Build IDS
cd $DIR/ids
./build

echo Build IPS
cd $DIR/ips
./build


