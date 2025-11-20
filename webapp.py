import streamlit as st
import pandas as pd
import time
import os
from webapp_utils import load_logs, load_alerts, load_performance, SHAP_FILE, SIEM_FILE
from webapp_plots import plot_traffic_over_time, plot_protocol_distribution, plot_attack_matrix, plot_performance_metrics, plot_correlation_heatmap

# --- Page Config ---
st.set_page_config(
    page_title="Cyber IDS SIEM | Enterprise Monitor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
    .metric-card {
        background-color: #262730;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #00FF99;
        margin-bottom: 20px;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #FAFAFA;
    }
    .metric-label {
        font-size: 1rem;
        color: #A0A0A0;
    }
    div.stButton > button {
        background-color: #00FF99;
        color: black;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #00CC7A;
        color: black;
        border: none;
    }
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# --- Data Loading ---
df = load_logs()
alerts = load_alerts()
perf = load_performance()

# --- Sidebar ---
with st.sidebar:
    st.title("Cyber IDS Engine")
    st.markdown("---")
    
    st.subheader("Filters")
    
    # Protocol Filter
    selected_protocols = []
    if df is not None:
        all_protocols = df["Protocol"].unique().tolist()
        selected_protocols = st.multiselect("Select Protocols", all_protocols, default=all_protocols)
    
    st.markdown("---")
    
    st.subheader("Control Panel")
    refresh_rate = st.slider("Auto-refresh (seconds)", 5, 60, 10)
    auto_refresh = st.checkbox("Enable Auto-refresh", value=False)
    
    if st.button("Manual Refresh"):
        st.cache_data.clear()
        
    st.markdown("---")
    
    # Report Download
    if os.path.exists(SIEM_FILE):
        with open(SIEM_FILE, "r") as f:
            siem_data = f.read()
        st.download_button(
            label="Download SIEM Report",
            data=siem_data,
            file_name="siem_security_report.txt",
            mime="text/plain"
        )
    
    st.markdown("---")
    st.info("**System Status**: 🟢 Online\n\n**Mode**: Detection & Mitigation")

# --- Filtering Logic ---
if df is not None:
    filtered_df = df[df["Protocol"].isin(selected_protocols)]
else:
    filtered_df = None


# --- Main Dashboard ---
st.title("Enterprise Security Operations Center")
st.markdown("### Real-time Network Monitoring & Threat Detection")

# Key Metrics Row
col1, col2, col3, col4 = st.columns(4)

total_packets = len(filtered_df) if filtered_df is not None else 0
total_alerts = len(alerts) if alerts else 0
accuracy = f"{perf.get('accuracy', 0):.2%}" if perf else "N/A"

def metric_card(label, value, col):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

metric_card("Filtered Packets", f"{total_packets:,}", col1)
metric_card("Threats Detected", total_alerts, col2)
metric_card("Model Accuracy", accuracy, col3)
metric_card("System Uptime", "99.98%", col4)

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["Network Traffic", "Security Alerts", "Model Intelligence", "Performance Metrics"])

with tab1:
    st.subheader("Network Traffic Analysis")
    if filtered_df is not None and not filtered_df.empty:
        row1_col1, row1_col2 = st.columns([2, 1])
        with row1_col1:
            fig_traffic = plot_traffic_over_time(filtered_df)
            if fig_traffic:
                st.plotly_chart(fig_traffic, use_container_width=True)
            else:
                st.info("Insufficient data for traffic plot.")

        with row1_col2:
            fig_proto = plot_protocol_distribution(filtered_df)
            if fig_proto:
                st.plotly_chart(fig_proto, use_container_width=True)
            else:
                st.info("Protocol data missing.")
        
        with st.expander("View Raw Traffic Logs (Filtered)", expanded=False):
            st.dataframe(filtered_df.head(100), use_container_width=True)
    else:
        st.warning("No traffic logs found matching current filters.")

with tab2:
    st.subheader("Threat Intelligence & Alerts")
    if alerts:
        col_alerts_1, col_alerts_2 = st.columns([2, 1])
        
        with col_alerts_1:
            # Display recent alerts with a nice styling
            for alert in alerts[::-1][:10]: # Last 10 alerts
                if "DDoS" in alert:
                    st.error(f"🔴 {alert.strip()}")
                elif "Port Scan" in alert:
                    st.warning(f"🟠 {alert.strip()}")
                elif "Brute Force" in alert:
                    st.warning(f"🟡 {alert.strip()}")
                else:
                    st.info(f"🔵 {alert.strip()}")
            
            if len(alerts) > 10:
                st.info(f"...and {len(alerts)-10} more alerts.")
                
        with col_alerts_2:
            fig_attacks = plot_attack_matrix(alerts)
            if fig_attacks:
                st.plotly_chart(fig_attacks, use_container_width=True)
            else:
                st.info("No threat data for visualization.")
    else:
        st.success("No active threats detected.")

with tab3:
    st.subheader("Explainable AI & Feature Analysis")
    
    col_xai_1, col_xai_2 = st.columns([1, 1])
    
    with col_xai_1:
        st.markdown("#### Feature Importance (SHAP)")
        if os.path.exists(SHAP_FILE):
             st.image(SHAP_FILE, use_column_width=True)
        else:
            st.info("SHAP explanation not available yet.")
            
    with col_xai_2:
        st.markdown("#### Feature Correlation Matrix")
        if filtered_df is not None:
             fig_corr = plot_correlation_heatmap(filtered_df.head(1000)) # Sample for performance
             if fig_corr:
                 st.plotly_chart(fig_corr, use_container_width=True)
             else:
                 st.info("Insufficient data for correlation analysis.")
        else:
            st.info("No data available for correlation.")

    st.markdown("---")
    st.markdown("""
    **Insight:** 
    - **Correlation Matrix** helps identify redundant features. High correlation between packet size and variance might indicate specific attack signatures.
    - **SHAP Values** explain individual model predictions, providing transparency for SOC analysts.
    """)

with tab4:
    st.subheader("Model Validation")
    if perf:
        row_perf_1, row_perf_2 = st.columns(2)
        with row_perf_1:
            fig_perf = plot_performance_metrics(perf)
            if fig_perf:
                st.plotly_chart(fig_perf, use_container_width=True)
            else:
                st.info("Performance metrics unavailable.")
        with row_perf_2:
            st.markdown("#### Metrics Breakdown")
            st.json(perf)
    else:
        st.info("Model performance data pending training completion.")

# Auto-refresh logic
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()
