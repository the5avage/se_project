from flask import jsonify

# Mock data for charging stations (replace with your actual data loading logic)
charging_stations = []

@app.route('/search_charging_station', methods=['POST'])
def search_charging_station():
    query = request.form.get('query', '').lower()
    results = [station for station in charging_stations if query in station['Address'].lower()]
    return render_template('search_results.html', results=results)

@app.route('/add_review', methods=['POST'])
def add_review():
    if 'user_id' not in session:
        return jsonify({"error": "You must be logged in to submit a review"}), 401

    station_id = request.form.get('station_id')
    rating = float(request.form.get('rating'))
    comment = request.form.get('comment', '')

    # Save the review to the database (mock implementation)
    print(f"Review added for station {station_id}: Rating={rating}, Comment={comment}")
    return jsonify({"message": "Review submitted successfully!"})

@app.route('/station_info/<int:station_id>')
def station_info(station_id):
    station = next((s for s in charging_stations if s['id'] == station_id), None)
    return jsonify(station) if station else jsonify({"error": "Station not found"}), 404

@app.route('/')
def home():
    global charging_stations  # Use the global variable

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

    # Assign unique IDs to each station
    charging_stations['id'] = range(1, len(charging_stations) + 1)

    # Convert to a list of dictionaries
    charging_stations = charging_stations[['id', 'Name', 'Address', 'Latitude', 'Longitude', 'PLZ']].to_dict('records')

    # Pass both GeoJSON and charging station data to the template
    return render_template('map.html', geojson=geojson, charging_stations=charging_stations)

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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            station_id INTEGER NOT NULL,
            rating REAL NOT NULL,
            comment TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (station_id) REFERENCES charging_stations (id)
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/add_review', methods=['POST'])
def add_review():
    if 'user_id' not in session:
        return jsonify({"error": "You must be logged in to submit a review"}), 401

    station_id = request.form.get('station_id')
    rating = float(request.form.get('rating'))
    comment = request.form.get('comment', '')

    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO reviews (user_id, station_id, rating, comment)
        VALUES (?, ?, ?, ?)
    ''', (session['user_id'], station_id, rating, comment))
    conn.commit()
    conn.close()

    return jsonify({"message": "Review submitted successfully!"})