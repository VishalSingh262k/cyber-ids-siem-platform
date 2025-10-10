# Importing libraries
import datetime

from analysis.mitre import MitreMapper


class AlertManager:

    def __init__(self):

        # Initialising alert list
        self.alerts = []

        # Initialising MITRE mapper
        self.mapper = MitreMapper()


    def raise_alert(self, source, attack_type, count):

        # Determining severity
        if count > 100:
            severity = "HIGH"
        else:
            severity = "MEDIUM"


        # Getting MITRE information
        mitre = self.mapper.map_attack(attack_type)


        # Creating alert record
        alert = {

            "Time": datetime.datetime.now(),

            "Source": source,

            "Attack": attack_type,

            "Count": count,

            "Severity": severity,

            "MITRE_Tactic": mitre.get("Tactic"),

            "MITRE_Technique": mitre.get("Technique"),

            "MITRE_Name": mitre.get("Name")
        }


        # Saving alert
        self.alerts.append(alert)

        # Printing alert
        print("\n ALERT")
        print(alert)


    def save_alerts(self, file_path="data/alerts.log"):

        # Writing alerts to file
        with open(file_path, "w") as f:

            for alert in self.alerts:

                f.write(str(alert) + "\n")
