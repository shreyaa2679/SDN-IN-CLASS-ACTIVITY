from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet.ethernet import ethernet
from pox.lib.addresses import EthAddr
from collections import defaultdict
import time

log = core.getLogger()

# MAC learning table for each switch
mac_tables = defaultdict(dict)

# Broadcast packet tracking
broadcast_cache = {}

# Duplicate suppression interval
BROADCAST_TIMEOUT = 2


class MACLearningController:

    def __init__(self, connection):
        self.connection = connection
        connection.addListeners(self)

        log.info("Controller connected to switch %s",
                 connection.dpid)

    def _handle_PacketIn(self, event):

        packet = event.parsed

        if not packet.parsed:
            return

        if packet.type == ethernet.LLDP_TYPE:
            return

        switch_id = event.dpid
        input_port = event.port

        source_mac = packet.src
        destination_mac = packet.dst

        table = mac_tables[switch_id]

        # Learn source MAC address
        if not source_mac.is_multicast:
            table[source_mac] = input_port

        log.info("MAC LEARNED: %s -> port %s",
                 source_mac, input_port)

        # Check whether destination MAC is already learned
        output_port = table.get(destination_mac)

        msg = of.ofp_packet_out()
        msg.data = event.ofp

        action = None

        if destination_mac.is_multicast or output_port is None:

            # Broadcast/unknown destination handling
            if packet.type == ethernet.ARP_TYPE or destination_mac.is_multicast:

                current_time = time.time()

                packet_key = (
                    switch_id,
                    source_mac,
                    destination_mac,
                    bytes(event.ofp.data)
                )

                last_seen = broadcast_cache.get(packet_key, 0)

                if current_time - last_seen < BROADCAST_TIMEOUT:
                    log.info("Duplicate broadcast suppressed")
                    return

                broadcast_cache[packet_key] = current_time

            action = of.ofp_action_output(
                port=of.OFPP_FLOOD
            )

            log.info("FLOOD: %s -> %s",
                     source_mac, destination_mac)

        else:

            if output_port == input_port:
                log.info("Packet received on destination port; dropping")
                return

            action = of.ofp_action_output(
                port=output_port
            )

            log.info("UNICAST: %s -> %s via port %s",
                     source_mac, destination_mac, output_port)

        msg.actions.append(action)

        self.connection.send(msg)


def launch():
    log.info("MAC Learning and Broadcast Suppression Controller started")

    def handle_connection(connection):
        MACLearningController(connection)

    core.openflow.addListenerByName(
        "ConnectionUp",
        lambda event: handle_connection(event.connection)
    )
