#!/bin/bash
screen -d -m bash -c '/etc/sdn/bin/karaf'
{
  while ! echo -n > /dev/tcp/localhost/8101; do
    sleep 5
  done
} 2>/dev/null

sshpass -p karaf ssh -p 8101 -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no karaf@localhost 'feature:install odl-dluxapps-applications odl-restconf odl-dluxapps-applications odl-openflowplugin-southbound odl-vtn-manager-rest odl-l2switch-hosttracker'
sshpass -p karaf ssh -p 8101 -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no karaf@localhost 'feature:repo-refresh'
#/usr/local/vtn/bin/vtn_stop
/usr/local/vtn/bin/vtn_start
