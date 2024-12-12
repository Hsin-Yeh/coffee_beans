#!/usr/bin/env python3

import sqlite3
import os

class CoffeeDB:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            print(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def create_tables(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS coffee_data (
                    id INTEGER PRIMARY KEY,
                    country TEXT,
                    region TEXT,
                    variety TEXT,
                    processing_method TEXT,
                    aroma REAL,
                    flavor REAL,
                    aftertaste REAL,
                    acidity REAL,
                    body REAL,
                    balance REAL,
                    uniformity REAL,
                    clean_cup REAL,
                    sweetness REAL,
                    overall REAL,
                    total_cup_points REAL,
                    moisture REAL
                )
            ''')

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS country_coordinates (
                    id INTEGER PRIMARY KEY,
                    country TEXT UNIQUE,
                    latitude REAL,
                    longitude REAL
                )
            ''')

            self.conn.commit()
            print("Tables created successfully")
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def get_all_countries(self):
        try:
            self.cursor.execute("SELECT DISTINCT country FROM coffee_data")
            return [row[0] for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error fetching countries: {e}")
            return []

    def get_country_info(self, country):
        try:
            query = """
            SELECT country, region, variety, processing_method, aroma, flavor, aftertaste,
                   acidity, body, balance, uniformity, clean_cup, sweetness, overall,
                   total_cup_points, moisture
            FROM coffee_data
            WHERE country = ?
            """
            self.cursor.execute(query, (country,))
            columns = [col[0] for col in self.cursor.description]
            return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error fetching country info: {e}")
            return []

    def get_country_coordinates(self, country):
        try:
            query = "SELECT latitude, longitude FROM country_coordinates WHERE country = ?"
            self.cursor.execute(query, (country,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error fetching country coordinates: {e}")
            return None

    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed")

# Example usage and testing
if __name__ == "__main__":
    db_path = "coffee_data.db"  # Adjust this path as needed
    db = CoffeeDB(db_path)

    # Test methods
    print("All countries:", db.get_all_countries())
    print("Info for Brazil:", db.get_country_info("Brazil"))
    print("Coordinates for Colombia:", db.get_country_coordinates("Colombia"))

    db.close()
