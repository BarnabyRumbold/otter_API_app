import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster

st.set_page_config(layout="wide")
st.sidebar.markdown("""
    <div style="text-align: center;">
        <img src="https://images.squarespace-cdn.com/content/v1/654a3265fcbd755384b0552f/5cc2d0e2-dd55-449f-ae3a-949ab6871318/MSlogo_colour_strapblue_L-800px.jpeg?format=1500w" alt="Logo" width="100"/>
    </div>
""", unsafe_allow_html=True)


st.write("### Otter Sightings Over Time (Time Series)")
st.markdown("*This graph shows a record of otter sightings over time from the earliest date in the data set. From this we can potentially look at changes in otter population numbers, though important consideration must be given to the fact that this is recorded otter sightings and not necessarily a reflection of otter populations.*")


# Access the loaded data from session state
df = st.session_state.get('otter_data')

# Assuming df is your DataFrame
# Example: df = pd.DataFrame({'year': [2020, 2021, 2022], 'sightings': [10, 15, 20]})

# Group data by year
sightings_by_year = df.groupby('year').size()

# Plot the time series
fig, ax = plt.subplots(figsize=(16, 6))  # Adjusting the width to fit Streamlit's layout

# Plot the sightings by year
sightings_by_year.plot(kind='line', ax=ax, marker='o', linestyle='-', linewidth=2, markersize=6, color='#333333')

# Customize plot to match minimalist and professional vibe
ax.set_xlabel('Year', fontsize=12, color='#333333')  # Dark grey labels
ax.set_ylabel('Number of Sightings', fontsize=12, color='#333333')  # Dark grey labels

# Remove gridlines for a cleaner look
ax.grid(False)

# Set background color to match page background
fig.patch.set_facecolor('#F7F7F7')  # Light grey background, matching the page background
ax.set_facecolor('#F7F7F7')  # Set the background of the plot area to match the page background

# Remove the top and right borders for a cleaner look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(0.5)  # Thin left border
ax.spines['bottom'].set_linewidth(0.5)  # Thin bottom border

# Display the plot in Streamlit
st.pyplot(fig)
st.markdown("*Showing live data from National Biodiversity Network Trust Atlas API.*")

