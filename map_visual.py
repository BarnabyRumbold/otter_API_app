import streamlit as st
import pandas as pd
import requests
import pydeck as pdk
import numpy as np
st.set_page_config(layout="wide")
st.sidebar.markdown("""
    <div style="text-align: center;">
        <img src="https://images.squarespace-cdn.com/content/v1/654a3265fcbd755384b0552f/5cc2d0e2-dd55-449f-ae3a-949ab6871318/MSlogo_colour_strapblue_L-800px.jpeg?format=1500w" alt="Logo" width="100"/>
    </div>
""", unsafe_allow_html=True)
st.write("### Otter Sightings Over Time (Map Visual)")
st.markdown("*This visual shows a series of maps of the UK over a 15 year period. The red dots indicate instances of an otter sighting, with a higher colour density indicating more sightings that year. From this we can potentially look at changes in otter population numbers geographically, though important consideration must be given to the fact that this is recorded otter sightings and not necessarily a reflection of otter populations.*")





# API URL for otter sightings
url = "https://records-ws.nbnatlas.org/occurrences/search"

# Params to search for otters
params = {
    "q": "otter",  # Search term for otter sightings
    "pageSize": 50000,  # Limit number of results
    "startDate": "2021-01-01",  # Start date for sightings
    "endDate": "2024-12-31"  # End date for sightings
}

# Make the request
response = requests.get(url, params=params)

# Check for successful request
if st.session_state.otter_data is not None:
    df = st.session_state.otter_data

    # Clean the data - change datetime to recognizable format
    df['eventDate'] = pd.to_datetime(df['eventDate'], unit='ms')
    
    # Order by date
    df_sorted = df.sort_values(by='eventDate', ascending=True)
    
    # Drop missing event dates and convert to datetime
    df = df_sorted.dropna(subset=['eventDate'])
    
    df['date'] = pd.to_datetime(df['eventDate'], unit='ms')
    df['year'] = df['date'].dt.year  # Extract year for filtering
    df['lat'] = df['decimalLatitude']
    df['lon'] = df['decimalLongitude']
    invalid_lat_lon = df[(df['lat'].abs() > 90) | (df['lon'].abs() > 180) | 
                    (~np.isfinite(df['lat'])) | (~np.isfinite(df['lon']))]
    
    df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
    df['lon'] = pd.to_numeric(df['lon'], errors='coerce')

    df = df.dropna(subset=['lat', 'lon'])
    df = df[(df['lat'].abs() <= 90) & (df['lon'].abs() <= 180)]
    df = df[np.isfinite(df['lat']) & np.isfinite(df['lon'])]

    # Select the years 2021, 2022, 2023, 2024 for the grid
    years = [2009, 2014, 2019, 2024]
    
    cols = st.columns(4)  

    for idx, year in enumerate(years):
        # Filter data by year
        df_filtered = df[df['year'] == year]

        # Group sightings by date and location
        sightings_by_year = df_filtered.groupby(['date', 'lat', 'lon']).size().reset_index(name='count')

        # Normalize the count to ensure no overflow in radius calculations
        sightings_by_year['radius'] = sightings_by_year['count'] * 700  # You can tweak this multiplier as needed

        # Create pydeck layer with adjusted radius
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=sightings_by_year,
            get_position='[lon, lat]',
            get_radius='radius',  # Use the normalized radius
            get_color='[200, 30, 0, 160]',
            pickable=True,
        )

        # Set the view to center over the UK
        view_state = pdk.ViewState(
            latitude=54.0,
            longitude=-2.0,
            zoom=5,
            pitch=0,
        )

        # Render the map in the appropriate column of the grid
        with cols[idx]:
            st.write(f"Otter Sightings in {year}")
            st.pydeck_chart(pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state=view_state,
                layers=[layer],
                height=400,  # Set a fixed height for all maps
            ))

else:
    st.error("Failed to load data.")
st.markdown("*Showing live data from National Biodiversity Network Trust Atlas API.*")

