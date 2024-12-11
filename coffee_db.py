#!/usr/bin/env python3

import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('coffee_database.db')
cursor = conn.cursor()

# Create the coffee_beans table if it doesn't exist
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
    ('Colombia', 'El Paraiso Diego Litchi', 'Light roasted'),
    ('Ethiopia', 'YIRGACHEFFE', 'Light roasted')
]

# Insert the coffee bean data into the database
cursor.executemany('''
    INSERT OR REPLACE INTO coffee_beans (country, bean_name, roast_level)
    VALUES (?, ?, ?)
''', coffee_data)

# Commit changes and close the connection
conn.commit()

# Verify the data was inserted correctly
cursor.execute("SELECT * FROM coffee_beans")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()

print("Database updated successfully.")
