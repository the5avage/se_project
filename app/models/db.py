import sqlite3
import hashlib

# Path to the database file
DB_PATH = 'db.sqlite3'

def get_connection():
    """
    Establishes and returns a connection to the SQLite database.
    """
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')

    # Create reviews table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            station_id INTEGER NOT NULL,
            rating REAL NOT NULL,
            comment TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (station_id) REFERENCES charging_stations (id)
        )
    ''')

    # Create charging stations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS charging_stations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            plz TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    
    
def hash_password(password):
    """
    Hashes a plaintext password using SHA-256 and returns the hashed value.
    """
    return hashlib.sha256(password.encode()).hexdigest()
