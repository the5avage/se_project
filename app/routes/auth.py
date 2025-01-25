from flask import Blueprint, request, session, render_template, redirect, url_for, flash
from app.repositories.user_repository import UserRepository
from app.models.db import hash_password


auth_bp = Blueprint('auth', __name__)
user_repo = UserRepository()

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hash_password(password)

        if user_repo.user_exists(username):
            return render_template('_error.html', message="Username already exists.")

        user_repo.create_user(username, password_hash)
        return render_template('_success.html', message="Registration successful! Please log in.")

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hash_password(password)

        user = user_repo.find_by_username_and_password(username, password_hash)
        if user:
            # Set the correct user_id in the session
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('map.home'))
        flash("Invalid credentials.")
        return redirect(url_for('auth.login'))
    return render_template('login.html')



@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    return redirect(url_for('map.home'))  # Redirect to the login page

