# import packages

import streamlit as st
import pandas as pd
import requests
import altair as alt
import matplotlib.pyplot as plt

# set page layout and add Mammal Society logo to sidebar
st.set_page_config(layout="wide")
# st.sidebar.markdown("""<div style="text-align: center;">
#         <img src="https://images.squarespace-cdn.com/content/v1/654a3265fcbd755384b0552f/5cc2d0e2-dd55-449f-ae3a-949ab6871318/MSlogo_colour_strapblue_L-800px.jpeg?format=1500w" alt="Logo" width="100"/>
#     </div>
# """, unsafe_allow_html=True)

# add page title
st.write("### Seasonal Changes")

# get data from session state
if st.session_state.otter_data is not None:
    df = st.session_state.otter_data

    # Clean the data - change datetime to recognizable format
    df['eventDate'] = pd.to_datetime(df['eventDate'], unit='ms')

    # Order by date
    df_sorted = df.sort_values(by='eventDate', ascending=True)

    # Remove blank rows
    df = df_sorted.dropna(subset=['eventDate'])

else:
    st.error("Failed to load data.")

# Step 1: Extract month from the date column
df_recent = df
df_recent['month'] = df_recent['eventDate'].dt.month

# Season function
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Autumn'

df_recent['season'] = df_recent['month'].apply(get_season)

# Step 2: Group by month or season and count sightings
seasonal_sightings = (
    df_recent.groupby(['season'])
    .size()
    .reset_index(name='sightings')
    .sort_values(by='sightings', ascending=False)
)

monthly_sightings = (
    df_recent.groupby(['month'])
    .size()
    .reset_index(name='sightings')
    .sort_values(by='month')
)

# Step 3: Visualize seasonal trends (using bar chart for season or month)
# Define a color palette with vibrant and subtle shades
color_palette = alt.Scale(domain=['Winter', 'Spring', 'Summer', 'Autumn'], 
                          range=['#B0E0E6', '#98FB98', '#F0E68C', '#D2B48C'])  # Light colors for each season

# Bar chart for seasonal sightings
seasonal_chart = alt.Chart(seasonal_sightings).mark_bar().encode(
    x=alt.X('season:N', sort=['Spring', 'Summer', 'Autumn', 'Winter']),
    y='sightings:Q',
    color=alt.Color('season:N', scale=color_palette),  # Apply the new color palette
    tooltip=['season:N', 'sightings:Q']
)

# Bar chart for monthly sightings
monthly_chart = alt.Chart(monthly_sightings).mark_bar().encode(
    x='month:O',
    y='sightings:Q',
    color=alt.Color('month:O', scale=alt.Scale(range=['#B0E0E6', '#98FB98', '#F0E68C', '#D2B48C', '#B0E0E6', '#98FB98', '#F0E68C', '#D2B48C', '#B0E0E6', '#98FB98', '#F0E68C', '#D2B48C'])),  # Same colors as seasonal
    tooltip=['month:O', 'sightings:Q']
)

# Display charts

st.markdown("*This graph shows seasonal changes in otter sightings over the last 10 years.*")
st.altair_chart(seasonal_chart, use_container_width=True)


st.markdown("*This graph shows monthly changes in otter sightings over the last 10 years.*")
st.altair_chart(monthly_chart, use_container_width=True)

# Note to provide information about where the data is coming from
st.markdown("*Showing live data from National Biodiversity Network Trust Atlas API.*")
