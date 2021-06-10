#!/bin/bash

mn -c && docker rm -f `docker ps -q` || true
