# Importing libraries
import streamlit as st
import pandas as pd
import json
import os

# File paths
LOG_FILE = "data/logs.csv"
ALERT_FILE = "data/alerts.log"
SIEM_FILE = "data/siem_report.txt"
SHAP_FILE = "data/shap_summary.png"
PERF_FILE = "data/performance.json"

# Loading logs
@st.cache_data
def load_logs():
    """Loads traffic logs from CSV efficiently."""
    if os.path.exists(LOG_FILE):
        try:
            df = pd.read_csv(LOG_FILE)
            
            # Synthesizing protocol if missing
            if "Protocol" not in df.columns:
                import numpy as np
                # Assigning protocols based on attack type or random for benign
                conditions = [
                    df["Attack_Type"] == "DDoS",
                    df["Attack_Type"] == "PortScan",
                    df["Attack_Type"] == "Exfiltration",
                    df["Attack_Type"] == "Benign"
                ]
                choices = ["UDP", "TCP", "DNS", "HTTP"]
                df["Protocol"] = np.select(conditions, choices, default="TCP")
                
            return df
        except Exception as e:
            st.error(f"Error loading logs: {e}")
            return None
    return None

# Loading alerts
def load_alerts():
    """Loads alerts from log file."""
    if os.path.exists(ALERT_FILE):
        with open(ALERT_FILE, "r") as f:
            return f.readlines()
    return []

# Loading performance
def load_performance():
    """Loads model performance metrics."""
    if os.path.exists(PERF_FILE):
        with open(PERF_FILE, "r") as f:
            return json.load(f)
    return None
