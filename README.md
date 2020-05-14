# ATMoS

ATMoS is a framework for applying [reinforcement learning](https://medium.com/machine-learning-for-humans/reinforcement-learning-6eacf258b265) to security management of [Software-defined Networks](https://medium.com/@blackvvine/sdn-part-1-what-is-software-defined-networking-sdn-and-why-should-i-know-about-it-e73a250ceccd).

# Concepts

TBA

<img src="https://github.com/ATMoS-Waterloo/ATMoS/blob/master/documentation/img/components.png" width=600 />

# Source Overview

This project uses OpenDaylight and Mininet to simulate the SDN infrastructure. More specifically, we [branched](https://github.com/blackvvine/gemelnet) [Containernet](https://containernet.github.io) which uses Docker containers for network hosts instead of LXC.

Host simulations, REST API server, and network gateways (with IDS/IPS enabled), are all implemented using Docker containers stored in the `images` folder.

```
.
├── conf
│   └── halsey.yml
├── documentation
├── images
│   ├── base
│   ├── benign-googler
│   ├── buildall.sh
│   ├── gw-base
│   ├── halsey
│   ├── host-base
│   ├── ids
│   ├── ips
│   ├── malish-apt
│   └── malish-syn
├── install
│   ├── odl.yml
│   └── setup-ubuntu.sh
├── lib
│   ├── bella
│   └── gemel
├── README.md
├── rl-agent
│   └── exp_001.py
└── topo
    ├── mytopo.py
    ├── run.sh
    └── vn.py
```

Two python libraries are available: `gemel` is a Python API for interacting with the SDN infrastructure (e.g. resetting host VN). `bella` is another Python API providing a wrapper for the REST API that is deployed to the network acting as the single source of interaction with the network by the RL agent. (`bella` makes calls to the Dockerized REST API server, codename Halsey, and Halsey uses `gemel` to implement low-level operations on the network)

Topology of the network is defined through `topo/mytopo.py`. Note that currently, this configuration should also be described in `conf/halsey.yml` and there is no way to have it automatically generated. (automation is back-logged for future)

Documentations about how everything works under the hood is provided in the docs folder. An example of training is also available at `rl-agent`.


# Installation

Our set-up is only tested on Ubuntu 16.04 LTS. Simply run the install script as root user:

```
git clone https://github.com/ATMoS-Waterloo/ATMoS.git
cd ATMoAS/install
sudo sh setup-ubuntu.sh
```

After dependencies were installed, build the necessary Docker containers:

```
cd ATMoS/images
./buildall
```

Note that these are the hosts used in the simulations in our submitted paper, and you can arbitrarily implement your own hosts and build your own topologies. The REST API (Halsey) and gateway images are meant to be reused.

Do keep in mind that 

# Usage

After the installation, launch the network:

```
cd ATMoS/topo
./run.sh
```

After the network is running, you can run RL agents using the `lib/bella` API. See the sample in `rl-agent`.

## Cleaning before running

If there are zombie containers left running from previous runs (e.g. if you kill the simulation non-gracefully), simply delete them using `docker rm` before running the new simulations. Additionally, can run `mn -C` to clean mininet boilerplate.

# Build your own

The hosts are designed in `images` as Docker containers. The topology in `topo` defines how these images are instantiated as host containers and connected to each other in the netowrk. The topology should also be described in `conf/halsey.yml` so that the API would know the network.

# Publication

Our [conference paper](http://rboutaba.cs.uwaterloo.ca/Papers/Conferences/2020/AkbariNOMS20.pdf) is accepted to be published in NOMS 2020 : IEEE/IFIP Network Operations and Management Symposium.

