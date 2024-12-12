#!/usr/bin/env python3

import streamlit as st
from streamlit_folium import folium_static
from coffee_map import CoffeeMap
from coffee_db import CoffeeDB

st.set_page_config(page_title="Coffee Bean Explorer", layout="wide")

db_path = "coffee_data.db"
coffee_map = CoffeeMap(db_path)
coffee_db = CoffeeDB(db_path)

st.title("Coffee Bean Explorer")

coffee_map.add_country_markers()
folium_static(coffee_map.get_map(), width=1000, height=600)

countries = coffee_db.get_all_countries()
selected_country = st.selectbox("Select a country", countries)

if selected_country:
    country_info = coffee_db.get_country_info(selected_country)
    if country_info:
        st.subheader(f"Coffee Information for {selected_country}")

        avg_info = {k: sum(float(d[k]) for d in country_info) / len(country_info)
                    for k in ['aroma', 'flavor', 'aftertaste', 'acidity', 'body', 'balance', 'overall', 'total_cup_points']}

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Average Aroma", f"{avg_info['aroma']:.2f}")
            st.metric("Average Flavor", f"{avg_info['flavor']:.2f}")
            st.metric("Average Aftertaste", f"{avg_info['aftertaste']:.2f}")
            st.metric("Average Acidity", f"{avg_info['acidity']:.2f}")
        with col2:
            st.metric("Average Body", f"{avg_info['body']:.2f}")
            st.metric("Average Balance", f"{avg_info['balance']:.2f}")
            st.metric("Average Overall", f"{avg_info['overall']:.2f}")
            st.metric("Average Total Cup Points", f"{avg_info['total_cup_points']:.2f}")

        st.subheader("Sample Entries")
        for i, entry in enumerate(country_info[:5]):
            with st.expander(f"Entry {i+1}"):
                st.write(f"Region: {entry['region']}")
                st.write(f"Variety: {entry['variety']}")
                st.write(f"Processing Method: {entry['processing_method']}")
                st.write(f"Total Cup Points: {entry['total_cup_points']}")

coffee_map.close_db()
coffee_db.close()
