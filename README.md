# AI-Based Cybersecurity Network Simulation & IDS

An end-to-end cybersecurity analytics platform that simulates enterprise network traffic and applies machine learning for intrusion detection, alerting, and threat intelligence mapping. This project simulates various network attack scenarios and uses an Ensemble Intrusion Detection System (IDS) to detect and classify malicious activities, mapping them to the MITRE ATT&CK framework.

---

## Features

- **Network Traffic Simulator**: Generates realistic benign and malicious network traffic using `simpy`.
- **Multi-Attack Modeling**: Simulates real-world cyber threats including DDoS, Brute Force, Port Scans, and Data Exfiltration.
- **Feature Engineering Pipeline**: Extracts statistical features from raw network logs for ML model training.
- **Ensemble Intrusion Detection System**: Combines Random Forest, Gradient Boosting, and Logistic Regression for robust threat detection.
- **MITRE ATT&CK Mapping**: Automatically maps detected alerts to specific MITRE T-Codes and Tactics.
- **SIEM-Style Reporting**: Generates comprehensive security reports.
- **Explainable AI (XAI)**: Uses SHAP (SHapley Additive exPlanations) to explain model predictions.
- **Interactive Dashboard**: A Streamlit-based web interface for real-time monitoring and analysis.

---

## MITRE ATT&CK Coverage

The system detects and maps the following adversary behaviors:

| Attack Type | MITRE Tactic | MITRE Technique ID | Technique Name |
| :--- | :--- | :--- | :--- |
| **DDoS** | Impact | **T1498** | Network Denial of Service |
| **Port Scan** | Reconnaissance | **T1046** | Network Service Discovery |
| **Brute Force** | Credential Access | **T1110** | Brute Force |
| **Exfiltration** | Exfiltration | **T1041** | Exfiltration Over C2 Channel |

---

## System Architecture

1.  **Simulator**: Generates raw network traffic logs.
2.  **Feature Engineering**: Converts logs into numerical features (packet rate, size entropy, etc.).
3.  **Ensemble IDS**: Predicts whether traffic is benign or malicious.
4.  **Alert Engine**: Filters predictions and generates alerts.
5.  **MITRE Mapper**: Contextualizes alerts with threat intelligence.
6.  **Reporting & XAI**: Produces SIEM reports and SHAP explanations.

---

## Tech Stack

- **Language**: Python 3.10+
- **Simulation**: SimPy
- **Data Manipulation**: Pandas, NumPy
- **Machine Learning**: Scikit-Learn (Random Forest, Gradient Boosting, Logistic Regression, Voting Classifier)
- **Explainability**: SHAP
- **Visualization**: Matplotlib, Streamlit

---

## Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/cyber_network_sim.git
    cd cyber_network_sim
    ```

2.  **Create a Virtual Environment (Optional but Recommended)**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

---

## Usage

### Run the Full Simulation Pipeline
This command runs the simulation, trains the IDS model, generates alerts, and creates reports.
```bash
python main.py
```
*The simulation runs for 1800 time steps by default.*

### Launch the Analytics Dashboard
After running the pipeline, visualize the results using the interactive dashboard.
```bash
streamlit run webapp.py
```

---

## Author

**Vishal Singh**

---

## License

This project is licensed under the **MIT License**.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.