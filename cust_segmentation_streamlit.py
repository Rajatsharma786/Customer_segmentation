import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.decomposition import PCA

# Page setup
st.set_page_config(page_title="Customer Segmentation Dashboard", layout="wide")
st.title("Customer Segmentation Analysis")

# Load data
df = pd.read_csv("data/user_behaviour_with_cluster.csv")

# Clean and setup
if 'cluster' not in df.columns:
    st.warning("Cluster labels not found. Please ensure clustering has been completed.")
    st.stop()

if 'segment_label' not in df.columns:
    segment_labels = {
        0: "Passive Browsers",
        1: "Non-Engaged Users",
        2: "Window Shoppers",
        3: "Loyal Buyers"
    }
    df['segment_label'] = df['cluster'].map(segment_labels)

# Sidebar filters
st.sidebar.header("Filter by Segment")
segments = df['segment_label'].unique().tolist()
selected_segments = st.sidebar.multiselect("Choose segments to view", segments, default=segments)

filtered_df = df[df['segment_label'].isin(selected_segments)]

# Display summary statistics
st.subheader("Segment Summary Statistics")
st.dataframe(
    filtered_df.groupby('segment_label')[
        ['views', 'purchases', 'conversion_rate', 'cart_to_purchase_ratio', 'sessions', 'avg_price']
    ].mean().round(2)
)

# 3D PCA plot using Plotly with fixed custom colors
st.subheader("PCA Cluster Visualization (3D Interactive)")
color_map = {
    "Passive Browsers": "red",
    "Non-Engaged Users": "blue",
    "Window Shoppers": "yellow",
    "Loyal Buyers": "pink"
}

fig3d = px.scatter_3d(
    filtered_df,
    x='pca1', y='pca2', z='pca3',
    color='segment_label',
    color_discrete_map=color_map,
    opacity=0.8,
    width=1000,
    height=700,
    title='Customer Segments (3D PCA Interactive)'
)

fig3d.update_traces(marker=dict(line=dict(width=0)))
st.plotly_chart(fig3d, use_container_width=True)

# Download filtered data
st.download_button(
    label="Download Filtered Segment Data as CSV",
    data=filtered_df.to_csv(index=False),
    file_name='filtered_segments.csv',
    mime='text/csv'
)
