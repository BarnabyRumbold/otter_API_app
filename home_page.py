# Import packages
from PIL import Image
import requests
from io import BytesIO
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


# Set up page layout with Mammal Society logo in the sidebar
st.set_page_config(layout="wide")
st.sidebar.markdown("""
    <div style="text-align: center;">
        <img src="https://images.squarespace-cdn.com/content/v1/654a3265fcbd755384b0552f/5cc2d0e2-dd55-449f-ae3a-949ab6871318/MSlogo_colour_strapblue_L-800px.jpeg?format=1500w" alt="Logo" width="100"/>
    </div>
""", unsafe_allow_html=True)


# Title and further information
st.write("### Welcome to the Otter Sightings App")
st.markdown("*Explore otter sightings across the UK through this interactive App. Leveraging data from the National Biodiversity Network (NBN) Atlas API, this tool provides valuable insights into otter populations, tracking their distribution, trends over time, and key conservation hotspots.*") 
st.markdown("*Whether you're a conservationist, researcher, or just an otter enthusiast, this dashboard offers a comprehensive view of otter sighting patterns to aid in better understanding and protecting these magnificent creatures.*")
st.markdown("*Please allow a few moments for each page to run.*")

# Set up columns 
col1, col2 = st.columns(2)

# Add content
with col1:

    # Add otter image
    otter_image_url = "https://images.squarespace-cdn.com/content/v1/654a3265fcbd755384b0552f/a9312805-4ca9-4994-9879-c6f9e1c5338f/Otter+on+Skye+by+Sophie+Hall+2.JPG?format=2500w"  # Replace with your actual otter image URL
    # Make a request to get the image
    response = requests.get(otter_image_url)

    # Open the image using Pillow
    image = Image.open(BytesIO(response.content))

    # Resize the image by setting the height to 400px (adjust as needed)
    new_height = 900
    new_width = int(image.width * (new_height / image.height))

    # Resize the image
    image_resized = image.resize((new_width, new_height))

    # Display the resized image
    st.image(image_resized)

with col2:
    
    # Provide information about the app and what it does/shows
    st.write("### Sightings Over Time (Time Series):")
    st.markdown("*Visualize otter sightings over time to potentially identify seasonal trends and long-term changes, including whether otter populations have shown signs of decline in certain areas.*")

    st.write("### Sightings Over Time (Map Visual):")
    st.markdown("*Visualise otter sightings over the last 20 years geographiaclly to understand potential changes in populations.*")
    
    st.write('### Seasonal Changes:')
    st.markdown('*Look at seasonal changes and monthly in otter sightings over the last 10 years.*')

    st.write("### Insights & Recommendations: ")
    st.markdown('*Understand summary statistics as well a the completeness and reliability of the sightings data.*')

    

# Note to provide information about where the data is coming from
st.markdown("*Showing live data from National Biodiversity Network Trust Atlas API.*")