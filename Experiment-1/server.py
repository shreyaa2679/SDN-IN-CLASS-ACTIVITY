from flask import Flask, request, jsonify
import subprocess
import re
import ipaddress
import time

app = Flask(__name__)

DEFAULT_THRESHOLD = 10000
previous_tx_bytes = {}
previous_time = {}


def run_command(command):
    """Execute a system command and return its output."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())

        return result.stdout

    except Exception as error:
        raise RuntimeError(str(error))


def validate_switch(switch):
    """Check whether the requested OVS bridge exists."""
    bridges = run_command(["ovs-vsctl", "list-br"]).splitlines()

    if switch not in bridges:
        raise ValueError("Switch does not exist: " + switch)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "running",
        "service": "SDN Traffic Monitoring REST API"
    })


@app.route("/switches", methods=["GET"])
def get_switches():
    try:
        output = run_command(["ovs-vsctl", "list-br"])
        switches = [item.strip() for item in output.splitlines()
                    if item.strip()]

        return jsonify({
            "switches": switches,
            "count": len(switches)
        })

    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.route("/stats", methods=["GET"])
def get_stats():
    try:
        switch = request.args.get("switch", "s1")
        threshold = int(
            request.args.get("threshold_bytes", DEFAULT_THRESHOLD)
        )

        if threshold < 0:
            return jsonify({"error": "Threshold cannot be negative"}), 400

        validate_switch(switch)

        output = run_command([
            "ovs-ofctl", "-O", "OpenFlow10",
            "dump-ports", switch
        ])

        current_tx_bytes = sum(
            int(value)
            for value in re.findall(r"tx_bytes=(\d+)", output)
        )

        current_time = time.time()

        old_bytes = previous_tx_bytes.get(switch, current_tx_bytes)
        old_time = previous_time.get(switch, current_time)

        interval_tx_bytes = max(0, current_tx_bytes - old_bytes)
        elapsed = max(current_time - old_time, 0.001)

        previous_tx_bytes[switch] = current_tx_bytes
        previous_time[switch] = current_time

        return jsonify({
            "switch": switch,
            "total_tx_bytes": current_tx_bytes,
            "interval_tx_bytes": interval_tx_bytes,
            "threshold_bytes": threshold,
            "threshold_exceeded": interval_tx_bytes > threshold,
            "interval_seconds": round(elapsed, 3)
        })

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.route("/block-icmp", methods=["POST"])
def block_icmp():
    try:
        data = request.get_json(silent=True) or {}

        switch = data.get("switch", "s1")
        src_ip = str(ipaddress.ip_address(data.get("src_ip", "")))
        dst_ip = str(ipaddress.ip_address(data.get("dst_ip", "")))

        threshold_exceeded = data.get("threshold_exceeded", False)

        if threshold_exceeded is not True:
            return jsonify({
                "success": False,
                "message": "Traffic threshold has not been exceeded."
            }), 400

        validate_switch(switch)

        flow = (
            f"priority=200,icmp,"
            f"nw_src={src_ip},nw_dst={dst_ip},actions=drop"
        )

        run_command([
            "ovs-ofctl", "-O", "OpenFlow10",
            "add-flow", switch, flow
        ])

        return jsonify({
            "success": True,
            "switch": switch,
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "action": "DROP",
            "protocol": "ICMP",
            "message": "ICMP traffic blocked successfully."
        })

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except Exception as error:
        return jsonify({"error": str(error)}), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
