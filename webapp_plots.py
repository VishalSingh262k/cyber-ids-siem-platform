# Importing libraries
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

# Plotting traffic over time
def plot_traffic_over_time(df):
    """Generates an interactive area chart for traffic volume over time."""
    if df is None or df.empty:
        return None
    
    # Ensuring Timestamp is handled correctly
    if "Timestamp" in df.columns:
        traffic_counts = df.groupby("Timestamp").size().reset_index(name="Packets")
        fig = px.area(
            traffic_counts, 
            x="Timestamp", 
            y="Packets",
            title="Real-time Network Traffic Volume",
            template="plotly_dark",
            markers=True
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Time Step",
            yaxis_title="Packet Count",
            hovermode="x unified"
        )
        return fig
    return None

# Plotting protocol distribution
def plot_protocol_distribution(df):
    """Generates a donut chart for protocol distribution."""
    if df is None or "Protocol" not in df.columns:
        return None
    
    proto_counts = df["Protocol"].value_counts().reset_index()  
    proto_counts.columns = ["Protocol", "Count"] # Explicitly renaming columns

    fig = px.pie(
        proto_counts, 
        values="Count", 
        names="Protocol", 
        title="Protocol Distribution",
        hole=0.4,
        template="plotly_dark",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)")
    return fig

# Plotting attack matrix
def plot_attack_matrix(alerts):
    """Visualizes attack types extracted from alerts."""
    if not alerts:
        return None
    
    # Parsing simple alerts for demo purposes to extract Attack Type
    attack_types = {"DDoS": 0, "Port Scan": 0, "Brute Force": 0, "Exfiltration": 0, "Benign": 0}
    
    for alert in alerts:
        for key in attack_types.keys():
            if key in alert:
                attack_types[key] += 1
    
    df_attacks = pd.DataFrame(list(attack_types.items()), columns=["Attack Type", "Count"])
    # Filtering out zero counts
    df_attacks = df_attacks[df_attacks["Count"] > 0]

    if df_attacks.empty:
        return None

    fig = px.bar(
        df_attacks, 
        x="Count", 
        y="Attack Type", 
        orientation='h',
        title="Detected Threats by Category",
        template="plotly_dark",
        color="Count",
        color_continuous_scale="Viridis"
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

# Plotting performance metrics
def plot_performance_metrics(perf_data):
    """Radar chart for model metrics."""
    if not perf_data:
        return None
    
    categories = ['Accuracy', 'Precision', 'Recall', 'Macro F1']
    values = [
        perf_data.get('accuracy', 0),
        perf_data.get('precision', 0),
        perf_data.get('recall', 0),
        perf_data.get('macro_f1', 0)
    ]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Model Performance',
        line_color='#00FF99'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=False,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        title="Model Performance Metrics"
    )
    
    return fig

# Plotting correlation heatmap      
def plot_correlation_heatmap(df):
    """Generates a correlation heatmap for numerical features."""
    if df is None or df.empty:
        return None
    
    # Selecting numerical columns only
    numerical_df = df.select_dtypes(include=['float64', 'int64'])
    
    if numerical_df.empty:
        return None
        
    # Calculating correlation matrix
    corr = numerical_df.corr()
    
    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title="Feature Correlation Matrix",
        template="plotly_dark",
        color_continuous_scale="Viridis"
    )
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)")
    return fig
