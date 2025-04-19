# Import packages
import streamlit as st

from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Set up pages, create titles and link to icons
pg = st.navigation([st.Page("home_page.py", title="Welcome"),
        st.Page("over_time.py", title="Sightings Over Time (Time Series)"),
        st.Page("map_visual.py", title="Sightings Over Time (Map Visual)"),
        st.Page("seasonal_changes.py", title="Seasonal Changes"),
        st.Page("recommendations.py", title="Insights & Recommendations")
        ])

import streamlit as st
import pandas as pd
import requests
import numpy as np

# Function to load data from API
def load_data():
        url = "https://records-ws.nbnatlas.org/occurrences/search"
        params = {
        "q": "otter",  # Search term for otter sightings
        "pageSize": 100000  # Limit number of results to speed up App performance
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
                data = response.json()
        if data.get("occurrences"):
                df = pd.json_normalize(data['occurrences'], errors='ignore')
                df_sorted = df.sort_values(by='eventDate', ascending=True)
                df = df_sorted.dropna(subset=['eventDate'])
                # There are some wierd date inputs, lets force these to numeric values
                df['date'] = pd.to_datetime(df['eventDate'], unit='ms', errors='coerce')
                # Rename lat and lon columns to allow mapping etc
                df['lat'] = df['decimalLatitude']
                df['lon'] = df['decimalLongitude']
                # Identifies invalid lat and lon values
                invalid_lat_lon = df[(df['lat'].abs() > 90) | (df['lon'].abs() > 180) |  (~np.isfinite(df['lat'])) | (~np.isfinite(df['lon']))]
                                
                # Again, force errors to resolve
                df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
                df['lon'] = pd.to_numeric(df['lon'], errors='coerce')

                # Drop null values
                df = df.dropna(subset=['lat', 'lon'])
                # Step 1: Filter sightings for the last 10 years
                today = datetime.today()
                ten_years_ago = today - timedelta(days=365 * 10)
                df_recent = df[df['date'] >= ten_years_ago]

                # Step 2: Find top 3 lat/lon hotspots (using the filtered data)
                top_coords = (
                df_recent.groupby(['lat', 'lon'])
                .size()
                .reset_index(name='Sightings')
                .sort_values(by='Sightings', ascending=False)
                .head(5)  # Only top 5
                )

                # Step 3: Reverse geocode after selecting top 3
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


                top_coords['Locality'] = top_coords.apply(lambda row: get_locality(row['lat'], row['lon']), axis=1)
                return df
        return None

# Check if data is already loaded into session state
if 'otter_data' not in st.session_state:
    st.session_state.otter_data = load_data()

# Check if data is loaded successfully
if st.session_state.otter_data is not None:
    df = st.session_state.otter_data
else:
    st.error("Failed to load data.")
    







pg.run()
