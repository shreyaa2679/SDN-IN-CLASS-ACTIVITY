#!/bin/bash

set -e

SWITCH="s1"
INTERFACE="s1-eth1"

echo "Configuring QoS for $SWITCH..."

# Create QoS queues
sudo ovs-vsctl -- set Port $INTERFACE qos=@newqos \
-- --id=@newqos create QoS type=linux-htb \
other-config:max-rate=10000000 \
queues:1=@control \
queues:2=@data \
-- --id=@control create Queue \
other-config:min-rate=4000000 \
other-config:max-rate=8000000 \
-- --id=@data create Queue \
other-config:min-rate=1000000 \
other-config:max-rate=4000000

echo "QoS queues configured successfully."
sudo ovs-vsctl list QoS
sudo ovs-vsctl list Queue
