# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
from streamlit.components.v1 import html

# --- Page Settings ---
st.set_page_config(
    page_title="Fertilizer Trend Analysis Dashboard",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Soft UI Styling ---
def local_css():
    st.markdown("""
        <style>
        .main {
            background-color: #f7f8fa;
        }
        .css-18e3th9 {
            padding: 2rem 1rem;
        }
        h1, h2, h3, h4 {
            color: #333333;
        }
        </style>
    """, unsafe_allow_html=True)

local_css()

# --- Fade-in Animation with Motion UI ---
html("""
<div style='animation: fadeIn 2s;'>
<script>
const fadeIn = `@keyframes fadeIn {from {opacity: 0;} to {opacity: 1;}}`;
const styleSheet = document.styleSheets[0];
styleSheet.insertRule(fadeIn, styleSheet.cssRules.length);
</script>
</div>
""", height=0)

# --- Load Dataset ---
@st.cache_data
def load_data():
    df = pd.read_csv("fertilizer_recommendation_dataset.csv")
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Options")
crop_types = df['Crop'].unique()
selected_crop = st.sidebar.multiselect("Select Crop Type", crop_types, default=crop_types)

# Filter based on sidebar
df_filtered = df[df['Crop'].isin(selected_crop)]

# --- Title and Header ---
st.markdown("""
# 🌾 Fertilizer Trend Analysis Dashboard
Discover hidden insights and trends from your agricultural data!
""")

# --- KPIs ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Entries", df_filtered.shape[0])
with col2:
    st.metric("Unique Crops", df_filtered['Crop'].nunique())
with col3:
    st.metric("Unique Fertilizers", df_filtered['Fertilizer Name'].nunique())

st.markdown("---")

# --- Trend Analysis Section ---

# Nutrient Trends
st.subheader("📈 Nutrient Trends Across Crops")

nutrients = ['Nitrogen (N)', 'Phosphorous (P)', 'Potassium (K)']
trend_data = df_filtered[nutrients + ['Crop']]
trend_summary = trend_data.groupby('Crop').mean().reset_index()

fig_trend = px.line(
    trend_summary.melt(id_vars='Crop', var_name='Nutrient', value_name='Value'),
    x='Crop', y='Value', color='Nutrient', markers=True,
    title='Average Nutrient Levels per Crop',
    template='plotly_white'
)
st.plotly_chart(fig_trend, use_container_width=True)

# pH vs EC Scatter
st.subheader("🌡️ Soil pH vs EC Analysis")

ph_ec_summary = df_filtered.groupby('Crop').agg({'pH': 'mean', 'EC': 'mean'}).reset_index()

fig_ph_ec_trend = px.scatter(
    ph_ec_summary,
    x='pH', y='EC', size_max=15, text='Crop',
    color='Crop', template='plotly_white',
    title='Average pH vs Electrical Conductivity (EC) by Crop'
)
fig_ph_ec_trend.update_traces(textposition='top center')
st.plotly_chart(fig_ph_ec_trend, use_container_width=True)

st.markdown("---")

# Most Recommended Fertilizers
st.subheader("🏆 Top 10 Most Recommended Fertilizers")

fertilizer_counts = df_filtered['Fertilizer Name'].value_counts().reset_index()
fertilizer_counts.columns = ['Fertilizer Name', 'Count']

fig_fert = px.bar(
    fertilizer_counts.head(10),
    x='Fertilizer Name', y='Count',
    color='Fertilizer Name',
    template='plotly_white',
    title='Top 10 Fertilizers Based on Usage'
)
st.plotly_chart(fig_fert, use_container_width=True)

# --- Footer ---
html("""
<div style='text-align:center;padding-top:30px;font-size:16px;color:#aaa;'>
Made with ❤️ using Streamlit and Plotly
</div>
""")
