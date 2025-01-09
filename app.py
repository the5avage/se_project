import sqlite3
import hashlib
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

# Routes
@app.route('/')
def home():
    return render_template('map.html')

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

@app.route('/map')
def map_view():
    return render_template('map.html')

if __name__ == '__main__':
    init_db()  # Initialize database schema
    app.run(debug=True)
