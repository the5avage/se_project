from flask import Blueprint, request, session, render_template, redirect, url_for, flash
from app.domains.events.auth_events import register_user, authenticate_user, logout_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Trigger the register_user event
        message = register_user(username, password)
        if message == "Username already exists.":
            return render_template('_error.html', message=message)
        return render_template('_success.html', message=message)

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Trigger the authenticate_user event
        user = authenticate_user(username, password)
        if user:
            # Set session data
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('map.home'))
        flash("Invalid credentials.")
        return redirect(url_for('auth.login'))
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    # Trigger the logout_user event
    logout_user(session)
    return redirect(url_for('map.home'))
