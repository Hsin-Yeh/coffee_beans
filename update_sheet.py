#!/usr/bin/env python3
# Coffee bean datasheet : https://docs.google.com/spreadsheets/d/1b8pcIIDMAoDf73Xqzg5i0373ZF1mMgiGYc2Efp96IhQ/edit?gid=0#gid=0

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time
import requests

# Setup Google Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open('Coffee Beans').sheet1

# Initialize geocoder
geolocator = Nominatim(user_agent="my_app")

def get_elevation(lat, lon):
    try:
        response = requests.get(f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}")
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            return data['results'][0]['elevation']
    except Exception as e:
        print(f"Error fetching elevation: {e}")
    return None

def get_location_info(country, region, village):
    try:
        location = geolocator.geocode(f"{village}, {region}, {country}", timeout=10)
        if location:
            elevation = get_elevation(location.latitude, location.longitude)
            return location.latitude, location.longitude, elevation

        location = geolocator.geocode(f"{region}, {country}", timeout=10)
        if location:
            elevation = get_elevation(location.latitude, location.longitude)
            return location.latitude, location.longitude, elevation

        return None, None, None
    except (GeocoderTimedOut, GeocoderUnavailable):
        time.sleep(1)
        return get_location_info(country, region, village)

# Get all values from the sheet
values = sheet.get_all_values()
headers = values[0]

# Find column indices
country_index = headers.index('Country')
region_index = headers.index('Region')
village_index = headers.index('Village')
altitude_index = headers.index('Altitude')
latitude_index = headers.index('Latitude')
longitude_index = headers.index('Longitude')

# Process each row
for i, row in enumerate(values[1:], start=2):
    country = row[country_index]
    region = row[region_index]
    village = row[village_index]

    if not row[altitude_index] or not row[latitude_index] or not row[longitude_index]:
        print(f"Fetching info for {village}, {region}, {country}")
        lat, lon, alt = get_location_info(country, region, village)

        if lat and lon:
            if not row[latitude_index]:
                sheet.update_cell(i, latitude_index + 1, lat)
            if not row[longitude_index]:
                sheet.update_cell(i, longitude_index + 1, lon)
            if alt is not None and not row[altitude_index]:
                sheet.update_cell(i, altitude_index + 1, alt)
            elif not row[altitude_index]:
                print(f"Altitude data not available for {village}, {region}, {country}")
            print(f"Updated information for {village}, {region}, {country}")
        else:
            print(f"Could not find information for {village}, {region}, {country}")

    time.sleep(1)

print("Processing complete!")
