import networkx as nx

class IntentSimulation:

    def __init__(self):
        self.graph = nx.Graph()
        self.bandwidth_required = 10

        # Network topology
        self.graph.add_edge("S1", "S2", bandwidth=100, active=True)
        self.graph.add_edge("S2", "S4", bandwidth=100, active=True)
        self.graph.add_edge("S1", "S3", bandwidth=50, active=True)
        self.graph.add_edge("S3", "S4", bandwidth=50, active=True)

        self.intent = {
            "source": "H1",
            "destination": "H2",
            "bandwidth": self.bandwidth_required,
            "state": "SUBMITTED",
            "path": []
        }

    def create_intent(self):
        print("\n--- POINT-TO-POINT INTENT ---")
        print("Source: H1 (00:00:00:00:00:01)")
        print("Destination: H2 (00:00:00:00:00:02)")
        print("Bandwidth requirement:", self.bandwidth_required, "Mbps")

        self.intent["state"] = "COMPILING"
        self.install_intent()

    def install_intent(self):
        try:
            path = nx.shortest_path(
                self.graph, "S1", "S4"
            )

            self.intent["path"] = path
            self.intent["state"] = "INSTALLED"

            print("\nIntent State:", self.intent["state"])
            print("Active Path:", " -> ".join(path))

        except nx.NetworkXNoPath:
            self.intent["state"] = "FAILED"
            print("Intent installation failed!")

    def simulate_link_failure(self):
        print("\n--- LINK FAILURE SIMULATION ---")

        if self.intent["path"]:
            failed_link = tuple(self.intent["path"][:2])

            self.graph[failed_link[0]][failed_link[1]]["active"] = False
            self.graph.remove_edge(*failed_link)

            print("Failed Link:", failed_link)

            print("\n--- INTENT RECOMPILATION ---")
            self.intent["state"] = "COMPILING"
            self.install_intent()

    def display_status(self):
        print("\n--- FINAL INTENT STATUS ---")
        print("Intent State:", self.intent["state"])
        print("Bandwidth:", self.intent["bandwidth"], "Mbps")

        if self.intent["path"]:
            print("Current Route:", " -> ".join(self.intent["path"]))


if __name__ == "__main__":
    simulation = IntentSimulation()

    simulation.create_intent()
    simulation.simulate_link_failure()
    simulation.display_status()
