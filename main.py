# Importing modules
import simpy
import pandas as pd
from simulator.network import NetworkTopology
from simulator.traffic import TrafficGenerator
from simulator.attacks import AttackSimulator
from simulator.monitor import NetworkMonitor
from analysis.explain import ExplainabilityEngine


from ml.features import FeatureExtractor
from ml.detector import AttackDetector

from analysis.performance import PerformanceAnalyzer
from analysis.siem_report import SIEMReporter

def main():

    # Initialising environment
    env = simpy.Environment()

    # Creating network
    topology = NetworkTopology()
    network = topology.create_topology()

    # Initialising monitor
    monitor = NetworkMonitor()

    # Creating traffic generator
    traffic = TrafficGenerator(env, network, monitor)

    # Creating attack simulator
    attacker = AttackSimulator(env, traffic)

    # Starting normal traffic
    env.process(
        traffic.generate_traffic("Client1", "Server")
    )

    # Starting attack traffic
    env.process(attacker.ddos_attack("Client2", "Server"))
    env.process(attacker.port_scan("Client2", "Server"))
    env.process(attacker.data_exfiltration("Client2", "Server"))
    env.process(attacker.brute_force("Client2", "Server"))
    env.process(attacker.ddos_attack("Client1", "Server"))
    env.process(attacker.brute_force("Client1", "Server"))
    env.process(attacker.port_scan("Client3", "Server"))
    env.process(attacker.data_exfiltration("Client3", "Server"))
    env.process(attacker.ddos_attack("Client4", "Server"))
    env.process(attacker.brute_force("Client4", "Server"))
    env.process(attacker.port_scan("Client5", "Server"))
    env.process(attacker.data_exfiltration("Client5", "Server"))

    # Running simulation
    env.run(until=1800)

    # Saving logs
    monitor.save_logs()

    # Extracting features
    extractor = FeatureExtractor()
    features = extractor.extract_features("data/logs.csv")

    # Training detector
    detector = AttackDetector()
    model, X_train = detector.train_model(features)

    # Analyzing performance
    analyzer = PerformanceAnalyzer()
    analyzer.analyze("data/logs.csv")

    # Generating SIEM report
    reporter = SIEMReporter()
    reporter.generate_report("data/logs.csv")

    # Generating SHAP explanation
    explainer = ExplainabilityEngine()
    explainer.explain_model(model, X_train)

if __name__ == "__main__":
    main()