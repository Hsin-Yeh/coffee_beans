#!/usr/bin/env python3
# Coffee bean data sheet: https://docs.google.com/spreadsheets/d/1b8pcIIDMAoDf73Xqzg5i0373ZF1mMgiGYc2Efp96IhQ/edit?gid=0#gid=0

import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from branca.colormap import LinearColormap

# Load world map data from the downloaded shapefile
world = gpd.read_file('ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp')

# Function to fetch data from Google Sheet
@st.cache_data
def get_coffee_data():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('Coffee Beans').sheet1
    data = sheet.get_all_values()
    headers = data.pop(0)
    return pd.DataFrame(data, columns=headers)

# Fetch coffee data
coffee_df = get_coffee_data()

# Convert 'Altitude' to numeric and handle missing values
coffee_df['Altitude'] = pd.to_numeric(coffee_df['Altitude'], errors='coerce')
# coffee_df['Altitude'] = coffee_df['Altitude'].fillna(coffee_df['Altitude'].mean())
coffee_df['Latitude'] = pd.to_numeric(coffee_df['Latitude'], errors='coerce')
coffee_df['Longitude'] = pd.to_numeric(coffee_df['Longitude'], errors='coerce')

# Aggregate data by country
country_data = coffee_df.groupby('Country').agg({
    'Village': 'count',
    'Altitude': 'mean'
}).reset_index()

# Merge coffee data with world data
world = world.merge(country_data, left_on='NAME', right_on='Country', how='left')
world['Coffee_Info'] = world.apply(
    lambda row: "; ".join(
        f"{village}: {flavors}" for village, flavors in zip(
            coffee_df[coffee_df['Country'] == row['NAME']]['Village'],
            coffee_df[coffee_df['Country'] == row['NAME']]['Flavors']
        )
    ) if row['NAME'] in coffee_df['Country'].values else "No data available",
    axis=1
)

# Create a Streamlit app
st.title('Interactive Coffee Map')

# Add this CSS hack to make the map responsive
st.markdown("""
<style>
[title~="st.iframe"] { width: 100% }
</style>
""", unsafe_allow_html=True)

# Create map layer options
map_layers = {
    'Number of Villages': 'Village',
    'Average Altitude': 'Altitude'
}

# Let user select map layer
selected_layer = st.selectbox('Select map layer:', list(map_layers.keys()))

# Create a Folium map
m = folium.Map(location=[15, 250], zoom_start=2, width='100%', height='1000px')

# Create color map
colormap = LinearColormap(colors=['yellow', 'orange', 'red'], vmin=world[map_layers[selected_layer]].min(), vmax=world[map_layers[selected_layer]].max())

# Add country polygons to the map
tooltip = folium.GeoJsonTooltip(
    fields=['NAME', 'Village', 'Altitude', 'Coffee_Info'],
    aliases=['Country:', 'Number of Villages:', 'Average Altitude (m):', 'Coffee Details:'],
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
        padding: 10px;
    """,
    max_width=300,
)

# Add country polygons to the map
folium.GeoJson(
    world,
    style_function=lambda feature: {
        'fillColor': colormap(feature['properties'][map_layers[selected_layer]]) if pd.notnull(feature['properties'][map_layers[selected_layer]]) else 'gray',
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.7,
    },
    tooltip=folium.GeoJsonTooltip(fields=['NAME', map_layers[selected_layer]], aliases=['Country:', f'{selected_layer}:']),
).add_to(m)

# Add markers for coffee bean locations
for idx, row in coffee_df.iterrows():
    tooltip_html = f"""
    <div style="font-family: Arial; font-size: 12px;">
        <b>{row['Country']} - {row['Village']}</b><br>
        Region: {row['Region']}<br>
        Process: {row['Process']}<br>
        Flavors: {row['Flavors']}<br>
        Altitude: {row['Altitude']} m
    </div>
    """

    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        tooltip=folium.Tooltip(tooltip_html, sticky=False),
        icon=folium.Icon(color='red', icon='coffee', prefix='fa')
    ).add_to(m)

# Add colormap to the map
colormap.add_to(m)

# Display the map using st_folium
output = st_folium(m, width=1980, height=500)

# Display country information when clicked
if output['last_active_drawing']:
    clicked_country = output['last_active_drawing']['properties']['NAME']
    st.write(f"You clicked on: {clicked_country}")

    # Display additional country information here
    country_info = world[world['NAME'] == clicked_country].iloc[0]
    st.write(f"Continent: {country_info['CONTINENT']}")
    st.write(f"Population: {country_info['POP_EST']:,.0f}")
    st.write(f"Region: {country_info['REGION_UN']}")
    st.write(f"Subregion: {country_info['SUBREGION']}")

    # Display coffee information if available
    coffee_info = coffee_df[coffee_df['Country'] == clicked_country]
    if not coffee_info.empty:
        st.write("Coffee Information:")
        st.write(f"Number of Villages: {len(coffee_info)}")
        st.write(f"Average Altitude: {coffee_info['Altitude'].mean():.2f} meters")
        st.write("Villages and Flavors:")
        for _, row in coffee_info.iterrows():
            st.write(f"- {row['Village']}: {row['Flavors']}")
    else:
        st.write("No coffee information available for this country.")
