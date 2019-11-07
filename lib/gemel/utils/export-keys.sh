#!/usr/bin/env bash

source ~/.bashrc

VM_NAME=$1

pubkey=$(cat ~/.ssh/id_rsa.pub)

gcloud compute ssh root@$VM_NAME -- "bash -c 'echo \"$pubkey\" >> ~/.ssh/authorized_keys'"

