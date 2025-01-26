import pytest
from app.domains.entities.db import get_connection, init_db

@pytest.fixture(scope="function")
def reset_database():
    """
    Reset the database by clearing all tables.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Delete all data from tables
    cursor.execute("DELETE FROM reviews;")
    cursor.execute("DELETE FROM users;")
    cursor.execute("DELETE FROM charging_stations;")
    conn.commit()
    conn.close()

@pytest.fixture(scope="function")
def client(reset_database):
    """
    Configure a test client with a reset database for each test.
    """
    from app import create_app
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client
