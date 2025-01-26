def test_register(client):
    # Ensure the username is unique for this test
    response = client.post('/auth/register', data={
        'username': 'unique_testuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert b"Registration successful" in response.data

def test_login(client):
    # First, register a user for the login test
    client.post('/auth/register', data={
        'username': 'testuser',
        'password': 'password123'
    })

    # Then, log in with the registered user credentials
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'password123'
    }, follow_redirects=True)  # Follow any redirects to ensure the response is valid
    assert response.status_code == 200
    assert b"Welcome" in response.data  # Update this based on your app's response

def test_add_review(client):
    # Mock user login
    with client.session_transaction() as session:
        session['user_id'] = 1
        session['username'] = 'testuser'

    # Add a review for a station
    response = client.post('/reviews/add_review', data={
        'station_id': 1,  # Ensure station ID exists in the test database
        'rating': 5,
        'comment': 'Great charging hub!'
    }, follow_redirects=True)  # Follow any redirects
    assert response.status_code == 200
    assert b"Review added successfully!" in response.data
