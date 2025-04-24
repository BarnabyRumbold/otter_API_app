import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
import altair as alt
import numpy as np
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from datetime import datetime, timedelta


# Set up page and add Mammal Soceity to sidebar
st.set_page_config(layout="wide")
# st.sidebar.markdown("""
#     <div style="text-align: center;">
#         <img src="https://images.squarespace-cdn.com/content/v1/654a3265fcbd755384b0552f/5cc2d0e2-dd55-449f-ae3a-949ab6871318/MSlogo_colour_strapblue_L-800px.jpeg?format=1500w" alt="Logo" width="100"/>
#     </div>
# """, unsafe_allow_html=True)

# Add title and page description
st.write("### Insights & Recommendations")
st.markdown("*This page provides an overview of statistics related to otter sightings.*")
st.markdown("*Summary statistics are provided alongside geographical locations showing top locations for otter sightings, potentially reflective of changes to otter populations. Finally some data quality observations are made for clarity as well as potential recommendations for future work. Important consideration must be given to the fact that this is recorded otter sightings and not necessarily a reflection of otter populations.*")

# get session state data
df = st.session_state.otter_data

# Order returned data frame by date
df_sorted = df.sort_values(by='eventDate', ascending=True)

# Lots of blank rows! Let's remove those with no date
df = df_sorted.dropna(subset=['eventDate'])

# There are some wierd date inputs, lets force these to numeric values
df['date'] = pd.to_datetime(df['eventDate'], unit='ms', errors='coerce')

# Rename lat and lon columns to allow mapping etc
df['lat'] = df['decimalLatitude']
df['lon'] = df['decimalLongitude']

# Identifies invalid lat and lon values
invalid_lat_lon = df[(df['lat'].abs() > 90) | (df['lon'].abs() > 180) | 
                (~np.isfinite(df['lat'])) | (~np.isfinite(df['lon']))]

# Again, force errors to resolve
df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
df['lon'] = pd.to_numeric(df['lon'], errors='coerce')

# Drop null lat/lon values
df = df.dropna(subset=['lat', 'lon'])

# Summarise otter sighting data
st.write("### Summary Statistics")
total_sightings = df.shape[0]
unique_days = df['date'].nunique()
sightings_per_day = total_sightings / unique_days if unique_days > 0 else 0
total_days = (pd.Timestamp.today() - df['date'].min()).days
sightings_per_total_days = total_sightings/total_days

# Set up some columns and create some summary statistics
col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"*Total Sightings:*  {total_sightings:,}")
col2.markdown(f"*Unique Observation Days:* {unique_days}")
col3.markdown(f"*Avg Sightings Per Observation Day:* {sightings_per_day:.2f}")
col4.markdown(f"*Avg Sighting Per Total Days:* {sightings_per_total_days:.2f}")

# Step 1: Filter sightings for the last 10 years - filter last ten years from data frame
today = datetime.today()
ten_years_ago = today - timedelta(days=365 * 10)
df['date'] = pd.to_datetime(df['date'])  # Ensure 'date' column is in datetime format
df_recent = df[df['date'] >= ten_years_ago]

# Step 2: Find top 5 lat/lon hotspots (using the filtered data)
top_coords = (
    df_recent.groupby(['lat', 'lon'])
    .size()
    .reset_index(name='Sightings')
    .sort_values(by='Sightings', ascending=False)
    .head(5)  # Only top 5
)

# Step 3: Reverse geocode after selecting top 5 to get nearby area/town etc
geolocator = Nominatim(user_agent="hotspot-locality-mapper")
reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1)

def get_locality(lat, lon):
    try:
        location = reverse((lat, lon), exactly_one=True, language='en')
        if location:
            for key in ['city', 'town', 'village', 'hamlet']:
                if key in location.raw['address']:
                    return location.raw['address'][key]
        return "Unknown"
    except:
        return "Unknown"

# Apply reverse geocoding to get area/town etc
top_coords['Locality'] = top_coords.apply(lambda row: get_locality(row['lat'], row['lon']), axis=1)


# Step 6: Show results by locality 
top_hotspots = (
    top_coords.groupby('Locality')['Sightings']
    .sum()
    .reset_index()
    .sort_values(by='Sightings', ascending=False)
)

col1, col2 = st.columns(2)
textColor = "#333333"  # From your TOML

with col1:
    st.write("### Top Otter Sightings Locations (Last 10 Years)")

    # Filter out unknown localities
    top_hotspots = top_hotspots[top_hotspots['Locality'] != 'Unknown']
    top_hotspots = top_hotspots[['Locality', 'Sightings']]

    # Create bar chart
    chart = alt.Chart(top_hotspots).mark_bar(
        color=textColor,
        size=8  # Smaller size = thinner bar
    ).encode(
        x=alt.X('Sightings:Q', title='Number of Sightings'),
        y=alt.Y('Locality:N', sort='-x', title='Locality'),
        tooltip=['Locality', 'Sightings']
    ).properties(
        width='container',
        height=300
    )

    st.altair_chart(chart, use_container_width=True)


# Add recommendations
with col2:
    
    st.write("### Recommendations")
    st.markdown("""
    - **Improve Monitoring** *Greater attention in areas with few sightings to assess whether absence/low numbers is due to low populations or underreporting*.
    - **Temporal Peaks** *Seasonal changes in spring and autumn suggest seasonal patterns worth exploring and monitoring*.
    - **Speak to Subject Matter Experts** *Speaking to experts could help to improve data accuracy*.
    - **Integrate Other Datasets** *The integration of other datasets would faciliate more accurate reporting and thus more conclusive insights*.
    - **Expanded Analysis** *Similar analysis of further species to identify broader biodiversity patterns*. 
    - **Causal Inference** *An exploration of reasons as to why these changes are taking place would help focus conservation efforts*. 
    """)

# Add data information 
col1, col2 = st.columns(2)
with col1:
    st.write("**Data Information**")
    st.markdown('*Data has been cleaned to remove invalid lat/lon values as well as those records missing a date. Data collection has also been limited to 100,000 rows to faciliate app performance. The data is accessed through a live connection to the National Biodiversity Network API. The data is refreshed each time the app is refreshed.*')

# Add contact and project information
with col2:
    st.write("**Contact and Project Information**")
    st.markdown("*For all contact enquiries please email: barnabyrumbold@hotmail.com*")
    st.markdown("*Collaboration is more than welcome, please find the GitHub repository [here](https://github.com/BarnabyRumbold/otter_API_dashboard)*")


st.markdown("*Showing live data from National Biodiversity Network Trust Atlas API.*")
