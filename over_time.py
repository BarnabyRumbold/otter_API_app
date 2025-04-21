# Import packages

import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
from PIL import Image
from io import BytesIO
import altair as alt
import numpy as np
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pydeck as pdk


# Set page layout
st.set_page_config(layout="wide")

# Add Mammal Society logo to sidebar
st.sidebar.markdown("""
    <div style="text-align: center;">
        <img src="https://images.squarespace-cdn.com/content/v1/654a3265fcbd755384b0552f/5cc2d0e2-dd55-449f-ae3a-949ab6871318/MSlogo_colour_strapblue_L-800px.jpeg?format=1500w" alt="Logo" width="100"/>
    </div>
""", unsafe_allow_html=True)

# Add title and page explanation
st.write("### Otter Sightings Over Time (Time Series)")
st.markdown("*This graph shows a record of otter sightings over time from the earliest date in the data set. From this we can potentially look at changes in otter population numbers, though important consideration must be given to the fact that this is recorded otter sightings and not necessarily a reflection of otter populations.*")


# Access the loaded data from session state from app.py
df = st.session_state.get('otter_data')

# Group data by year
sightings_by_year = df.groupby('year').size()

# Plot the time series
fig, ax = plt.subplots(figsize=(16, 6))  

# Plot the sightings by year
sightings_by_year.plot(kind='line', ax=ax, marker='o', linestyle='-', linewidth=2, markersize=6, color='#333333')

# Customize plot to match minimalist and professional vibe
ax.set_xlabel('Year', fontsize=12, color='#333333')  # Dark grey labels
ax.set_ylabel('Number of Sightings', fontsize=12, color='#333333')  # Dark grey labels

# Remove gridlines for a cleaner look
ax.grid(False)

# Set background color to match page background
fig.patch.set_facecolor('#F7F7F7')  
ax.set_facecolor('#F7F7F7')  

# Remove the top and right borders for a cleaner look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(0.5)  # Thin left border
ax.spines['bottom'].set_linewidth(0.5)  # Thin bottom border

# Display the plot 
st.pyplot(fig)

# Note to provide information about where the data is coming from
st.markdown("*Showing live data from National Biodiversity Network Trust Atlas API.*")

