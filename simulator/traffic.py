# Importing required libraries
import random
import simpy

# Defining traffic generator class
class TrafficGenerator:

    def __init__(self, env, network, monitor):
        # Initialising environment
        self.env = env

        # Storing network graph
        self.network = network

        # Storing monitor
        self.monitor = monitor

    def generate_traffic(self, src, dst, is_attack=False):

        while True:

            # Generating packet size
            packet_size = random.randint(400, 1500)

            # Generating delay
            delay = random.uniform(0.2, 0.8)

            # Logging packet
            self.monitor.log_packet(
                src, dst, packet_size, "Benign", self.env.now
            )

            # Waiting before next packet
            yield self.env.timeout(delay)
