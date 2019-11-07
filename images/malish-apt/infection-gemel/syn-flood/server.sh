#!/bin/bash

DIR="$(dirname $0)"

source $DIR/config.sh

cd "$SERVE_DIR"
python3 -m http.server 8001

