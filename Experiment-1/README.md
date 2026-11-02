# Experiment 1: SDN Traffic Monitoring and ICMP Blocking

## Objective
To monitor network traffic statistics and demonstrate
selective ICMP traffic blocking using Software Defined Networking.

## Technologies
- Python
- Flask REST API
- Open vSwitch
- OpenFlow 1.0
- Mininet

## Architecture
Mininet Hosts
     |
Open vSwitch
     |
Flask REST API
     |
Traffic Monitoring and ICMP Flow Management

## Setup

Install Open vSwitch and Mininet.

Create and activate a Python virtual environment:

python3 -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

## Start the Mininet topology

sudo mn --topo single,2 --mac \
--controller remote,ip=127.0.0.1,port=6633 \
--switch ovsk,protocols=OpenFlow10

## Start the REST API

In another terminal:

cd ~/SDN-IN-CLASS-ACTIVITY/Experiment-1

sudo ./venv/bin/python server.py

## API Endpoints

### Health check
GET /health

### List switches
GET /switches

### Monitor traffic
GET /stats?switch=s1&threshold_bytes=10000

### Block ICMP
POST /block-icmp

Example JSON:

{
  "switch": "s1",
  "src_ip": "10.0.0.1",
  "dst_ip": "10.0.0.2",
  "threshold_exceeded": true
}

## Result
The REST API retrieves switch information and traffic
statistics. When the specified threshold condition is met,
an ICMP DROP flow can be installed in the Open vSwitch.

## Screenshots
Store experiment screenshots in the screenshots folder.
