#!/usr/bin/env python3

import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('coffee_database.db')
cursor = conn.cursor()

# Create the coffee_beans table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS coffee_beans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        country TEXT NOT NULL,
        bean_name TEXT NOT NULL,
        roast_level TEXT NOT NULL
    )
''')

# Define the coffee bean data to be added
coffee_data = [
    ('Colombia', 'El Paraiso Diego Litchi', 'Light roasted')
]

# Insert the coffee bean data into the database
cursor.executemany('''
    INSERT INTO coffee_beans (country, bean_name, roast_level)
    VALUES (?, ?, ?)
''', coffee_data)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database created, table set up, and coffee bean data added successfully.")
