#!/bin/bash

set -e

DIR=$(dirname $0)

$DIR/../images/buildall.sh

echo ""
echo "Built all images."
echo ""

cp $DIR/../conf/halsey.yml $DIR/../images/halsey/halsey-api/src/

halsey_id=$($DIR/../images/halsey/halsey-api/run.sh daemon)

python3 $DIR/mytopo.py

docker kill $halsey_id

