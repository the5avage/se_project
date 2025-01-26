from app.entities.db import hash_password
from app.repositories.user_repository import UserRepository

user_repo = UserRepository()

# Event: Register a new user
def register_user(username, password):
    """
    Registers a new user by storing their hashed password in the database.

    Args:
        username (str): The username of the user.
        password (str): The plaintext password of the user.
    
    Returns:
        str: Success or error message.
    """
    password_hash = hash_password(password)
    if user_repo.user_exists(username):
        return "Username already exists."
    user_repo.create_user(username, password_hash)
    return "Registration successful! Please log in."

# Event: Authenticate user during login
def authenticate_user(username, password):
    """
    Authenticates a user by verifying their username and password.

    Args:
        username (str): The username of the user.
        password (str): The plaintext password of the user.
    
    Returns:
        dict or None: User object if authentication succeeds, otherwise None.
    """
    password_hash = hash_password(password)
    user = user_repo.find_by_username_and_password(username, password_hash)
    return user

# Event: Logout user
def logout_user(session):
    """
    Logs out the current user by clearing their session.

    Args:
        session (dict): The session object to clear.
    """
    session.pop('user_id', None)
    session.pop('username', None)
