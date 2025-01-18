import sqlite3
import hashlib
import pandas as pd
import geopandas as gpd
from shapely import wkt
import json
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Initialize Database
def init_db():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Hash Password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def home():
    # Load the GeoJSON data
    with open('output.geojson', 'r') as f:
        geojson = json.load(f)

    # Load the charging station dataset
    df_lstat = pd.read_excel("datasets/Ladesaeulenregister_SEP.xlsx", header=10)

    # Normalize the 'Ort' column and filter for Berlin
    df_lstat['Ort'] = df_lstat['Ort'].str.strip().str.lower()
    df_lstat = df_lstat.loc[df_lstat['Ort'] == 'berlin']

    # Extract and rename relevant columns
    charging_stations = df_lstat[['Anzeigename (Karte)', 'Straße', 'Hausnummer', 'Breitengrad', 'Längengrad', "PLZ"]]

    # Drop rows with missing latitude or longitude
    charging_stations = charging_stations.dropna(subset=['Breitengrad', 'Längengrad'])

    # Check for invalid latitude and longitude values
    # invalid_lat = charging_stations['Breitengrad'].str.contains('[^0-9,.-]', regex=True)
    # invalid_lng = charging_stations['Längengrad'].str.contains('[^0-9,.-]', regex=True)

    # # Drop rows with invalid coordinates
    # charging_stations = charging_stations[~invalid_lat & ~invalid_lng]

    # Convert latitude and longitude to float
    charging_stations['Latitude'] = charging_stations['Breitengrad'].str.replace(',', '.').astype(float)
    charging_stations['Longitude'] = charging_stations['Längengrad'].str.replace(',', '.').astype(float)

    # Filter out invalid coordinates
    charging_stations = charging_stations[
        (charging_stations['Latitude'].between(-90, 90)) &
        (charging_stations['Longitude'].between(-180, 180))
    ]

    # Combine "Straße" and "Hausnummer" into a single address string
    charging_stations['Address'] = charging_stations['Straße'] + ' ' + charging_stations['Hausnummer'].astype(str)

    # Rename columns to match expected keys
    charging_stations = charging_stations.rename(columns={
        'Anzeigename (Karte)': 'Name',
        'Breitengrad': 'Latitude',
        'Längengrad': 'Longitude'
    })

    # Convert to a list of dictionaries
    charging_stations = charging_stations[['Name', 'Address', 'Latitude', 'Longitude', 'PLZ']].to_dict('records')

    # Pass both GeoJSON and charging station data to the template
    return render_template('map.html', geojson=geojson, charging_stations=charging_stations)

@app.route('/map')
def map_view():
    with open('output.geojson', 'r') as f:
        geojson = json.load(f)
    return render_template('map.html', geojson=geojson)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hash_password(password)

        try:
            conn = sqlite3.connect('db.sqlite3')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
            conn.commit()
            conn.close()
            return render_template('_success.html', message="Registration successful! Please log in.")
        except sqlite3.IntegrityError:
            return render_template('_error.html', message="Username already exists. Try a different one.")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hash_password(password)

        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ? AND password_hash = ?', (username, password_hash))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            return render_template('_success.html', message="Login successful!")
        else:
            return render_template('_error.html', message="Invalid credentials. Please try again.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return render_template('_success.html', message="Logged out successfully.")



if __name__ == '__main__':
    init_db()  # Initialize database schema
    app.run(debug=True)
