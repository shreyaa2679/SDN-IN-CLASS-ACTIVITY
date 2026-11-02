# Experiment 3: Traffic Slicing and QoS Management in SDN

## Aim
To implement traffic classification and Quality of Service (QoS) management in a Software-Defined Networking (SDN) environment using POX, Mininet, and Open vSwitch.

## Tools and Technologies
- Ubuntu
- Mininet
- POX Controller
- Open vSwitch (OVS)
- Python 3
- OpenFlow 1.0

## Network Topology
A single-switch topology was created with two hosts connected to one Open vSwitch.

- Host 1 (h1): 10.0.0.1
- Host 2 (h2): 10.0.0.2
- Switch: s1

## Implementation

### 1. Traffic Classification
The POX controller identifies TCP traffic based on destination port numbers.

- Control traffic: TCP port 5001, assigned to Queue 1.
- Data traffic: TCP port 5002, assigned to Queue 2.

### 2. QoS Queue Configuration
Open vSwitch queues were configured on the switch interface connected to h2 (`s1-eth2`).

| Queue | Traffic Type | Minimum Rate | Maximum Rate |
|---|---|---:|---:|
| Queue 1 | Control | 4 Mbps | 8 Mbps |
| Queue 2 | Data | 1 Mbps | 4 Mbps |

The overall interface maximum rate was configured as 10 Mbps.

### 3. Traffic Transmission
TCP servers were started on h2 using ports 5001 and 5002. Traffic was generated from h1 and transmitted to the corresponding servers.

### 4. Verification
The following commands were used to verify the implementation:

- `pingall` – verifies network connectivity.
- `ovs-ofctl -O OpenFlow10 queue-stats s1` – displays queue statistics.
- `ovs-ofctl -O OpenFlow10 dump-flows s1` – displays installed OpenFlow rules.

## Results

- The POX controller successfully connected to the switch.
- Network connectivity was verified with 0% packet loss.
- Control and data traffic were classified into separate queues.
- Queue statistics showed nonzero packet and byte counters.
- OpenFlow rules successfully assigned TCP port 5001 to Queue 1 and port 5002 to Queue 2.

The experiment demonstrates traffic classification and queue assignment. Bandwidth guarantees under congestion were not separately benchmarked.

## Screenshots

The `screenshots` folder contains:

1. POX controller startup
2. Network connectivity
3. Server listening status
4. Traffic transmission
5. QoS queue statistics
6. OpenFlow flow rules

## Conclusion

Traffic slicing and QoS queue management were successfully demonstrated using an SDN environment. The controller classified traffic based on TCP destination ports and assigned it to separate queues configured in Open vSwitch.
