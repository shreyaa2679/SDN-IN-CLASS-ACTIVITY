# Experiment 2: MAC Learning and Broadcast Storm Prevention

## Objective
To implement MAC address learning and forwarding using a
Software Defined Networking controller and demonstrate
duplicate broadcast packet suppression.

## Technologies
- POX Controller
- Mininet
- Open vSwitch
- OpenFlow 1.0
- Python

## Controller Features
1. Learns source MAC addresses.
2. Maintains a MAC-to-port mapping.
3. Forwards packets to known destinations.
4. Floods packets when the destination is unknown.
5. Suppresses repeated duplicate broadcast packets
   within a configured time interval.

## Execution

### 1. Start the POX controller

cd ~/pox

python3 -u ./pox.py log.level --DEBUG \
misc.mac_learning

If using this repository's controller file, copy it into
the POX modules directory first:

cp ~/SDN-IN-CLASS-ACTIVITY/Experiment-2/mac_learning.py \
~/pox/pox/misc/

### 2. Start Mininet

sudo mn --topo single,2 --mac \
--controller remote,ip=127.0.0.1,port=6633 \
--switch ovsk,protocols=OpenFlow10

### 3. Test connectivity

mininet> pingall

### 4. Inspect controller output

Observe MAC LEARNED, FLOOD, UNICAST and
Duplicate broadcast suppressed messages in the POX terminal.

## Expected Result
The controller learns host MAC addresses and forwards
traffic using the learned MAC-to-port mapping.
Repeated identical broadcast packets from the same source
are suppressed within the configured time interval.

## Screenshots
Store experiment screenshots in the screenshots directory.
