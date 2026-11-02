from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()


class QoSController:

    def __init__(self):
        core.openflow.addListeners(self)
        log.info("Traffic Slicing and QoS Controller Started")

    def _handle_ConnectionUp(self, event):

        log.info("Switch connected: %s", event.dpid)

        # CONTROL SLICE - TCP destination port 5001
        control_flow = of.ofp_flow_mod()
        control_flow.priority = 200

        control_flow.match.dl_type = 0x0800
        control_flow.match.nw_proto = 6
        control_flow.match.tp_dst = 5001

        control_flow.actions.append(
            of.ofp_action_enqueue(
                port=2,
                queue_id=1
            )
        )

        event.connection.send(control_flow)

        # DATA SLICE - TCP destination port 5002
        data_flow = of.ofp_flow_mod()
        data_flow.priority = 100

        data_flow.match.dl_type = 0x0800
        data_flow.match.nw_proto = 6
        data_flow.match.tp_dst = 5002

        data_flow.actions.append(
            of.ofp_action_enqueue(
                port=2,
                queue_id=2
            )
        )

        event.connection.send(data_flow)

        log.info("Control and Data traffic queues configured")


def launch():
    core.registerNew(QoSController)
