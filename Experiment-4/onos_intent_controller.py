import json
import os
import sys
import requests
from requests.auth import HTTPBasicAuth

BASE = os.getenv("ONOS_URL", "http://127.0.0.1:8181/onos/v1")
APP_ID = "org.onosproject.cli"

AUTH = HTTPBasicAuth(
    os.getenv("ONOS_USER", "onos"),
    os.getenv("ONOS_PASSWORD", "rocks")
)

def call(method, path, **kwargs):
    response = requests.request(
        method,
        BASE + path,
        auth=AUTH,
        timeout=15,
        headers={
            "Accept": "application/json",
        },
        **kwargs
    )

    print(f"{method} {path}: HTTP {response.status_code}")

    if not response.ok:
        print(response.text)
        response.raise_for_status()

    return response

def check_services():
    endpoints = [
        "/devices",
        "/hosts",
        f"/applications/{APP_ID}"
    ]

    for endpoint in endpoints:
        print("\n---", endpoint, "---")
        print(json.dumps(call("GET", endpoint).json(), indent=2))

def show_intents():
    print("\n--- INTENT STATUS ---")
    data = call("GET", "/intents").json()
    print(json.dumps(data, indent=2))

    for intent in data.get("intents", []):
        print("Intent:", intent.get("key"))
        print("State:", intent.get("state"))

if __name__ == "__main__":
    try:
        check_services()
        show_intents()

    except requests.RequestException as error:
        print("\nONOS request failed:", error)
        print("HTTP 503 indicates that a required ONOS service is unavailable.")
        sys.exit(1)
