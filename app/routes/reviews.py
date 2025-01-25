from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from app.repositories.review_repository import ReviewRepository

reviews_bp = Blueprint('reviews', __name__)
review_repo = ReviewRepository()

@reviews_bp.route('/add_review', methods=['GET'])
def add_review_page():
    # Check if the user is logged in
    if 'user_id' not in session:
        flash("You must be logged in to add a review.")
        return redirect(url_for('auth.login'))
    return render_template('add_review.html')

@reviews_bp.route('/add_review', methods=['POST'])
def add_review():
    if 'user_id' not in session or 'username' not in session:
        flash("You must be logged in to add a review.")
        return redirect(url_for('auth.login'))

    station_id = request.form.get('station_id')
    rating = request.form.get('rating')
    comment = request.form.get('comment')

    if not station_id or not rating or not comment:
        flash("All fields are required.")
        return redirect(url_for('reviews.add_review'))

    user_id = session['user_id']
    username = session['username']  # Fetch the username from the session
    review_repo.create_review(user_id=user_id, username=username, station_id=station_id, rating=rating, comment=comment)

    flash("Review added successfully!")
    return redirect(url_for('reviews.add_review'))

@reviews_bp.route('/user_reviews', methods=['GET'])
def user_reviews():
    if 'username' not in session:
        flash("You must be logged in to view your reviews.")
        return redirect(url_for('auth.login'))

    username = session['username']  # Get the logged-in user's username
    print("karo",username)
    reviews = review_repo.get_reviews_by_username(username)

    return render_template('user_reviews.html', reviews=reviews)

