def test_add_review(client):
    # Mock login
    with client.session_transaction() as session:
        session['user_id'] = 1
        session['username'] = 'testuser'

    response = client.post('/reviews/add_review', data={
        'station_id': 1,
        'rating': 5,
        'comment': 'Great charging hub!'
    }, follow_redirects=True)  # Follow redirects

    assert response.status_code == 200
    assert b"Review added successfully" in response.data


def test_user_reviews(client):
    # Mock login
    with client.session_transaction() as session:
        session['user_id'] = 1
        session['username'] = 'testuser'

    # Add a review for the user
    client.post('/reviews/add_review', data={
        'station_id': 1,
        'rating': 5,
        'comment': 'Great charging hub!'
    }, follow_redirects=True)

    # Fetch the user's reviews
    response = client.get('/reviews/user_reviews')
    assert response.status_code == 200
    assert b"My Reviews" in response.data
    assert b"Great charging hub!" in response.data  # Ensure the comment is displayed
