#!/usr/bin/env python3

from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('coffee_map.html')

@app.route('/get_coffee/<country>')
def get_coffee(country):
    conn = sqlite3.connect('coffee_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT bean_name, roast_level FROM coffee_beans WHERE country = ?', (country,))
    beans = cursor.fetchall()
    conn.close()
    return jsonify(beans)

if __name__ == '__main__':
    app.run(debug=True)
