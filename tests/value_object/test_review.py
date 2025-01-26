import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.domains.value_objects import Review

def test_review_initialization():
    """Test the initialization of the Review class."""
    review = Review(
        id=1,
        user_id=101,
        username="test_user",
        station_id=5,
        rating=4.5,
        comment="Great station!"
    )

    assert review.id == 1
    assert review.user_id == 101
    assert review.username == "test_user"
    assert review.station_id == 5
    assert review.rating == 4.5
    assert review.comment == "Great station!"

def test_review_repr():
    """Test the __repr__ method of the Review class."""
    review = Review(
        id=1,
        user_id=101,
        username="test_user",
        station_id=5,
        rating=4.5,
        comment="Great station!"
    )

    expected_repr = "<Review by User test_user for Station 5>"
    assert repr(review) == expected_repr
