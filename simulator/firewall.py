# Importing required libraries
from collections import defaultdict
import time


# Defining firewall class
class Firewall:

    def __init__(self):

        # Initialising blocked sources
        self.blocked_sources = set()

        # Initialising packet counters
        self.packet_counter = defaultdict(int)

        # Defining rate limit
        self.rate_limit = 100   # packets per window

        # Defining time window
        self.time_window = 5    # seconds


    def inspect_packet(self, src, attack_type, timestamp):

        # Blocking if source is already blacklisted
        if src in self.blocked_sources:
            return False


        # Counting packets
        window = int(timestamp // self.time_window)
        key = (src, window)

        self.packet_counter[key] += 1


        # Applying rate limiting
        if self.packet_counter[key] > self.rate_limit:

            # Blocking source
            self.blocked_sources.add(src)

            return False


        # Allow first few malicious packets for detection
        if attack_type != "Benign":

            # Blocking only after threshold
            if self.packet_counter[key] > 500:
                self.blocked_sources.add(src)
                return False

        return True