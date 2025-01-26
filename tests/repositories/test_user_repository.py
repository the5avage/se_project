import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.domains.entities.user import User
from app.domains.repositories.user_repository import UserRepository

@pytest.fixture
def user_repository():
    db_path = 'test_db.sqlite3'
    if os.path.exists(db_path):
        os.remove(db_path)

    repo = UserRepository(db_path=db_path)
    # Create the users table
    repo.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    return repo

# Test creating a user
def test_create_user(user_repository):
    user_repository.create_user("test_user", "hashed_password")
    result = user_repository.fetchall("SELECT * FROM users")
    assert len(result) == 1
    assert result[0][1] == "test_user"
    assert result[0][2] == "hashed_password"

# Test finding a user by username and password
def test_find_by_username_and_password(user_repository):
    user_repository.create_user("test_user", "hashed_password")
    user = user_repository.find_by_username_and_password("test_user", "hashed_password")
    assert user is not None
    assert user.username == "test_user"
    assert user.password_hash == "hashed_password"

# Test checking if a user exists
def test_user_exists(user_repository):
    user_repository.create_user("test_user", "hashed_password")
    user = user_repository.user_exists("test_user")
    assert user is not None
    assert user.username == "test_user"

    non_existent_user = user_repository.user_exists("nonexistent_user")
    assert non_existent_user is None

# Test finding a user by ID
def test_find_by_id(user_repository):
    user_repository.create_user("test_user", "hashed_password")
    result = user_repository.fetchall("SELECT * FROM users")
    user_id = result[0][0]

    user = user_repository.find_by_id(user_id)
    assert user is not None
    assert user.id == user_id
    assert user.username == "test_user"

    non_existent_user = user_repository.find_by_id(9999)
    assert non_existent_user is None