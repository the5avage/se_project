import pytest
import datetime
from domains.value_objects.Address import Address
from domains.value_objects.Review import Review
from domains.entities.ChargingStation import ChargingStation
from domains.repositories.ChargingStationRepository import ChargingStationRepository  # Adjust import path
import sqlite3

def create_test_schema(connection):
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE charging_stations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        street TEXT NOT NULL,
        city TEXT NOT NULL,
        state TEXT NOT NULL,
        zip_code TEXT NOT NULL,
        country TEXT NOT NULL,
        capacity INTEGER NOT NULL
    );
    """)
    cursor.execute("""
    CREATE TABLE reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rating REAL NOT NULL,
        comment TEXT,
        created_at TEXT NOT NULL,
        reviewer_id INTEGER NOT NULL,
        charging_station_id INTEGER NOT NULL,
        FOREIGN KEY (charging_station_id) REFERENCES charging_stations (id)
    );
    """)
    connection.commit()

@pytest.fixture
def db_connection():
    """Fixture to provide a fresh in-memory SQLite database."""
    connection = sqlite3.connect(":memory:")
    create_test_schema(connection)
    yield connection
    connection.close()


@pytest.fixture
def repo(db_connection):
    """Fixture to provide a ChargingStationRepository instance."""
    return ChargingStationRepository(db_connection)

def test_add_charging_station(repo):
    address = Address("Main St", "Springfield", "IL", "62701", "USA")
    review = Review(rating=4.5, comment="Excellent service!", created_at=datetime.now(), reviewer_id=1)
    station = ChargingStation(id=None, address=address, capacity=10, reviews=[review])

    repo.add(station)

    retrieved_station = repo.get(1)
    assert retrieved_station is not None
    assert retrieved_station.address.street == "Main St"
    assert retrieved_station.capacity == 10
    assert len(retrieved_station.reviews) == 1
    assert retrieved_station.reviews[0].rating == 4.5

def test_get_nonexistent_charging_station(repo):
    retrieved_station = repo.get(999)  # ID 999 does not exist
    assert retrieved_station is None

def test_add_multiple_charging_stations(repo):
    address1 = Address("Main St", "Springfield", "IL", "62701", "USA")
    address2 = Address("Second Ave", "Metropolis", "NY", "10001", "USA")
    station1 = ChargingStation(id=None, address=address1, capacity=10)
    station2 = ChargingStation(id=None, address=address2, capacity=5)

    repo.add(station1)
    repo.add(station2)

    retrieved_station1 = repo.get(1)
    retrieved_station2 = repo.get(2)
    assert retrieved_station1 is not None
    assert retrieved_station2 is not None
    assert retrieved_station1.address.city == "Springfield"
    assert retrieved_station2.address.city == "Metropolis"

def test_delete_charging_station(repo):
    address = Address("Main St", "Springfield", "IL", "62701", "USA")
    station = ChargingStation(id=None, address=address, capacity=10)

    repo.add(station)

    repo.delete(1)

    retrieved_station = repo.get(1)
    assert retrieved_station is None

def test_add_reviews_to_charging_station(repo):
    address = Address("Main St", "Springfield", "IL", "62701", "USA")
    review1 = Review(rating=4.5, comment="Great service!", created_at=datetime.now(), reviewer_id=1)
    review2 = Review(rating=3.0, comment="Okay experience.", created_at=datetime.now(), reviewer_id=2)
    station = ChargingStation(id=None, address=address, capacity=10, reviews=[review1, review2])

    repo.add(station)

    retrieved_station = repo.get(1)
    assert len(retrieved_station.reviews) == 2
    assert retrieved_station.reviews[0].comment == "Great service!"
    assert retrieved_station.reviews[1].rating == 3.0
