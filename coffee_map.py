#!/usr/bin/env python3

import folium
from folium.plugins import MarkerCluster
from coffee_db import CoffeeDB

class CoffeeMap:
    def __init__(self, db_path):
        self.db = CoffeeDB(db_path)
        self.map = folium.Map(location=[0, 0], zoom_start=2)
        self.marker_cluster = MarkerCluster().add_to(self.map)

    def add_country_markers(self):
        countries = self.db.get_all_countries()
        for country in countries:
            coordinates = self.db.get_country_coordinates(country)
            if coordinates:
                self._add_country_marker(country, coordinates)

    def _add_country_marker(self, country, coordinates):
        country_info = self.db.get_country_info(country)
        if country_info:
            popup_content = self._create_popup_content(country_info)
            folium.Marker(
                location=coordinates,
                popup=folium.Popup(popup_content, max_width=300),
                tooltip=country
            ).add_to(self.marker_cluster)

    def _create_popup_content(self, country_info):
        info = country_info[0]
        content = f"""
        <b>Country:</b> {info['country']}<br>
        <b>Region:</b> {info['region']}<br>
        <b>Variety:</b> {info['variety']}<br>
        <b>Processing Method:</b> {info['processing_method']}<br>
        <b>Aroma:</b> {info['aroma']:.2f}<br>
        <b>Flavor:</b> {info['flavor']:.2f}<br>
        <b>Aftertaste:</b> {info['aftertaste']:.2f}<br>
        <b>Acidity:</b> {info['acidity']:.2f}<br>
        <b>Body:</b> {info['body']:.2f}<br>
        <b>Balance:</b> {info['balance']:.2f}<br>
        <b>Overall:</b> {info['overall']:.2f}<br>
        <b>Total Cup Points:</b> {info['total_cup_points']:.2f}<br>
        """
        return content

    def get_map(self):
        return self.map

    def close_db(self):
        self.db.close()
