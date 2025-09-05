# Importing libraries
import pandas as pd
from simulator.firewall import Firewall

# Defining monitoring class
class NetworkMonitor:

    def __init__(self):
        # Initialising log storage
        self.logs = []

        # Initialising firewall
        self.firewall = Firewall()

    def log_packet(self, src, dst, size, attack_type, time):

        # Inspecting packet using firewall
        allowed = self.firewall.inspect_packet(
            src, attack_type, time
        )

        # Dropping blocked packets
        if not allowed:
            return

        # Logging allowed packet
        direction = "OUT" if src.startswith("Client") else "IN"
        self.logs.append([
            src, dst, size, attack_type, time, direction
        ])

    def save_logs(self):

        # Creating dataframe
        df = pd.DataFrame(
            self.logs,
            columns=[
                    "Source", "Destination",
                    "Packet_Size", "Attack_Type",
                    "Timestamp", "Direction"
                ]
        )

        # Saving to CSV
        df.to_csv("data/logs.csv", index=False)
