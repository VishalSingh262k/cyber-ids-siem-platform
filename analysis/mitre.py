# MITRE ATT&CK Mapping

MITRE_MAPPING = {

    "DDoS": {
        "Tactic": "Impact",
        "Technique": "T1498",
        "Name": "Network Denial of Service"
    },

    "PortScan": {
        "Tactic": "Reconnaissance",
        "Technique": "T1046",
        "Name": "Network Service Discovery"
    },

    "BruteForce": {
        "Tactic": "Credential Access",
        "Technique": "T1110",
        "Name": "Brute Force"
    },

    "Exfiltration": {
        "Tactic": "Exfiltration",
        "Technique": "T1041",
        "Name": "Exfiltration Over C2 Channel"
    },

    "Benign": {
        "Tactic": "Normal",
        "Technique": "N/A",
        "Name": "Legitimate Activity"
    }
}


class MitreMapper:

    def map_attack(self, label):

        return MITRE_MAPPING.get(label, {})
