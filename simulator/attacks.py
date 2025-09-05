# Importing libraries
import random
import simpy


# Defining attack simulator class
class AttackSimulator:

    def __init__(self, env, traffic_gen):

        # Initialising environment
        self.env = env

        # Storing traffic generator
        self.traffic_gen = traffic_gen


    def ddos_attack(self, src, dst):

        # Simulating DDoS flooding
        while True:

            # Generating large packets
            packet_size = random.randint(1200, 2000)

            # Logging DDoS packet
            self.traffic_gen.monitor.log_packet(
                src, dst, packet_size, "DDoS", self.env.now
            )

            # Very small delay
            yield self.env.timeout(random.uniform(0.5, 1.5))


    def port_scan(self, src, dst):

        # Simulating port scanning behavior
        for port in range(20, 1024):

            # Generating small probe packets
            packet_size = random.randint(100, 300)

            # Logging scan packet
            self.traffic_gen.monitor.log_packet(
                src, dst, packet_size, "PortScan", self.env.now
            )

            # Moderate delay
            yield self.env.timeout(random.uniform(0.5, 1.5))


    def data_exfiltration(self, src, dst):

        # Simulating data theft
        for _ in range(1000):

            # Generating medium packets
            packet_size = random.randint(800, 1200)

            # Logging exfiltration
            self.traffic_gen.monitor.log_packet(
                src, dst, packet_size, "Exfiltration", self.env.now
            )

            # Slow stealthy transfer
            yield self.env.timeout(random.uniform(0.5, 1.5))


    def brute_force(self, src, dst):

        # Simulating login attacks
        for _ in range(1500):

            # Generating authentication packets
            packet_size = random.randint(200, 400)

            # Logging brute force
            self.traffic_gen.monitor.log_packet(
                src, dst, packet_size, "BruteForce", self.env.now
            )

            # Fast retries
            yield self.env.timeout(random.uniform(0.5, 1.5))
