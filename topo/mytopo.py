#!/usr/bin/env python

import time

from mininet.net import Containernet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel

from functools import partial

from vn import install_vns, init_vns


setLogLevel('info')

net = Containernet(controller=partial(RemoteController, ip='172.17.0.1', port=6633), autoSetMacs=True)

info('*** Adding controller\n')

net.addController('c0')

info('*** Adding gateways\n')

gw1 = net.addDocker('gw1', ip='210.0.0.200', mac="00:00:00:00:00:01", dimage="mg-ids", pubnet=True)
gw2 = net.addDocker('gw2', ip='210.0.0.200', mac="00:00:00:00:00:02", dimage="mg-ips", pubnet=True)

info('*** Adding simulations\n')

h1 = net.addDocker('h1', ip='210.0.0.101', mac="00:00:00:00:00:03", dimage="mg-benign-googler")
h2 = net.addDocker('h2', ip='210.0.0.102', mac="00:00:00:00:00:04", dimage="mg-host-base")

info('*** Adding switches\n')

s1 = net.addSwitch('sw1')
s2 = net.addSwitch('sw2')

info('*** Creating links\n')

net.addLink(h1, s1)
net.addLink(gw1, s1)

net.addLink(h2, s2)
net.addLink(gw2, s2)

net.addLink(s1, s2, latency=200)

# net.addLink(s1, s2, cls=TCLink, delay='100ms', bw=1)

info('*** Starting network\n')
net.start()

# info('*** Testing connectivity\n')
# net.ping([h1, h2])

info('*** Starting nodes\n')
h1.start()
h2.start()
gw1.start()
gw2.start()

info('*** Initiating virtual nets\n')
install_vns()
init_vns()

info('*** Running CLI\n')
CLI(net)

info('*** Stopping network')
net.stop()



