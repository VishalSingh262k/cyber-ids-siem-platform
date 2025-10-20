# Importing libraries
import pandas as pd
import datetime


# Defining SIEM reporter
class SIEMReporter:

    def generate_report(self, file_path):

        # Loading logs
        df = pd.read_csv(file_path)

        # Report time
        now = datetime.datetime.now()

        report = []

        report.append(" SIEM SECURITY REPORT \n")
        report.append(f"Generated: {now}\n\n")

        # Summary
        total = len(df)
        attacks = df[df["Attack_Type"] != "Benign"]

        report.append(f"Total Packets: {total}\n")
        report.append(f"Total Attacks: {len(attacks)}\n\n")

        # Attack stats
        report.append("Attack Breakdown:\n")

        breakdown = attacks["Attack_Type"].value_counts()

        for k, v in breakdown.items():
            report.append(f"{k}: {v}\n")

        # Top attackers
        report.append("\nTop Attack Sources:\n")

        top = attacks["Source"].value_counts().head(5)

        for k, v in top.items():
            report.append(f"{k}: {v}\n")

        # Saving report
        with open("data/siem_report.txt", "w") as f:
            f.writelines(report)

        print("SIEM Report Generated: data/siem_report.txt")
