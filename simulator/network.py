# Importing required libraries
import networkx as nx

# Defining network topology class
class NetworkTopology:

    def __init__(self):
        # Initialising graph
        self.graph = nx.Graph()

    def create_topology(self):

        # Adding nodes
        self.graph.add_nodes_from([
            "Client1", "Client2", "Server",
            "Router", "Firewall"
        ])

        # Adding links
        self.graph.add_edges_from([
            ("Client1", "Router"),
            ("Client2", "Router"),
            ("Router", "Firewall"),
            ("Firewall", "Server")
        ])

        return self.graph
