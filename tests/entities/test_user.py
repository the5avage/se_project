import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.domains.entities.user import User


def test_user_initialization():
    # Arrange
    user_id = 1
    username = "testuser"
    password_hash = "hashedpassword"

    # Act
    user = User(user_id, username, password_hash)

    # Assert
    assert user.id == user_id
    assert user.username == username
    assert user.password_hash == password_hash

def test_user_repr():
    # Arrange
    user_id = 1
    username = "testuser"
    password_hash = "hashedpassword"
    user = User(user_id, username, password_hash)

    # Act
    repr_string = repr(user)

    # Assert
    assert repr_string == "<User id=1 username=testuser>"
