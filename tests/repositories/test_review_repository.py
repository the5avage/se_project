import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app.domains.repositories.base_repository import BaseRepository
from app.domains.value_objects.review import Review
from app.domains.repositories.review_repository import ReviewRepository

@pytest.fixture
def review_repository():
    db_path = 'test_db.sqlite3'
    if os.path.exists(db_path):
        os.remove(db_path)

    repo = ReviewRepository(db_path=db_path)
    # Initialize the database schema
    repo.execute('''
        CREATE TABLE reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            station_id INTEGER,
            rating INTEGER,
            comment TEXT
        )
    ''')
    return repo

# Test create_review
def test_create_review(review_repository):
    review_repository.create_review(1, "test_user", 101, 5, "Great station!")
    reviews = review_repository.fetchall("SELECT * FROM reviews")
    assert len(reviews) == 1
    assert reviews[0][1] == 1  # user_id
    assert reviews[0][2] == "test_user"
    assert reviews[0][3] == 101  # station_id
    assert reviews[0][4] == 5  # rating
    assert reviews[0][5] == "Great station!"

# Test delete_review
def test_delete_review(review_repository):
    review_repository.create_review(1, "test_user", 101, 5, "Great station!")
    review_repository.create_review(2, "another_user", 102, 3, "Average.")
    review_repository.delete_review(1)
    reviews = review_repository.fetchall("SELECT * FROM reviews")
    assert len(reviews) == 1
    assert reviews[0][0] == 2  # Only the second review remains

# Test get_reviews_by_username
def test_get_reviews_by_username(review_repository):
    review_repository.create_review(1, "test_user", 101, 5, "Great station!")
    review_repository.create_review(2, "test_user", 102, 4, "Nice station.")
    review_repository.create_review(3, "another_user", 103, 3, "Okay station.")
    reviews = review_repository.get_reviews_by_username("test_user")
    print(reviews)
    assert len(reviews) == 2
    assert reviews[0]["station_id"] == 101
    assert reviews[1]["comment"] == "Nice station."
    assert reviews[0]["station_ranking"] == 5
