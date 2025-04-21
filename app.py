# This file sets up the app and also does the initial data scrape using an API

# Import packages
import streamlit as st
import pandas as pd
import requests
import numpy as np

# Set up pages, create titles
pg = st.navigation([st.Page("home_page.py", title="Welcome"),
        st.Page("over_time.py", title="Sightings Over Time (Time Series)"),
        st.Page("map_visual.py", title="Sightings Over Time (Map Visual)"),
        st.Page("seasonal_changes.py", title="Seasonal Changes"),
        st.Page("recommendations.py", title="Insights & Recommendations")
        ])


# Function to load data from API
def load_data():
    url = "https://records-ws.nbnatlas.org/occurrences/search"
    params = {
        "q": "otter",  # Search term for otter sightings
        "pageSize": 200000  # Limit number of results to speed up App performance
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("occurrences"):
            df = pd.json_normalize(data['occurrences'], errors='ignore')
            df_sorted = df.sort_values(by='eventDate', ascending=True)
            df = df_sorted.dropna(subset=['eventDate'])
            return df
    return None

# Load data into session state
if 'otter_data' not in st.session_state:
    st.session_state.otter_data = load_data()

# Check if data is loaded successfully
if st.session_state.otter_data is not None:
    df = st.session_state.otter_data
else:
    st.error("Failed to load data.")
    
# This line runs all of the pages outlined above
pg.run()
