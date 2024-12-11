#!/usr/bin/env python3

from flask import Flask, render_template, request, jsonify
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

@app.route('/add_coffee', methods=['POST'])
def add_coffee():
    data = request.json
    conn = sqlite3.connect('coffee_database.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO coffee_beans (country, bean_name, roast_level, notes)
            VALUES (?, ?, ?, ?)
        ''', (data['country'], data['bean_name'], data['roast_level'], data['notes']))
        conn.commit()
        return jsonify({'success': True, 'message': 'Coffee added successfully'})
    except sqlite3.Error as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
