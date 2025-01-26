# handle database operations related to users
from app.repositories.base_repository import BaseRepository
from app.entities.user import User

from app.repositories.base_repository import BaseRepository
from app.entities.user import User

class UserRepository(BaseRepository):
    def create_user(self, username, password_hash):
        """
        Creates a new user in the database.
        """
        query = '''
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
        '''
        try:
            print(f"Creating user: {username}, {password_hash}")  # Debugging
            self.execute(query, (username, password_hash))
            print("User created successfully.")  # Debugging
        except Exception as e:
            print(f"Error creating user: {e}")  # Debugging

    def find_by_username_and_password(self, username, password_hash):
        """
        Finds a user by their username and password hash.
        Returns a User object or None if no match is found.
        """
        query = '''
            SELECT id, username, password_hash
            FROM users
            WHERE username = ? AND password_hash = ?
        '''
        try:
            print(f"Querying user: {username}, {password_hash}")  # Debugging
            result = self.fetchone(query, (username, password_hash))
            print(f"Query result: {result}")  # Debugging
            if result:
                return User(id=result[0], username=result[1], password_hash=result[2])
        except Exception as e:
            print(f"Error finding user: {e}")  # Debugging
        return None

    def user_exists(self, username):
        """
        Checks if a user exists by their username.
        Returns True if the user exists, otherwise False.
        """
        query = '''
            SELECT id, username, password_hash
            FROM users
            WHERE username = ?
        '''
        try:
            print(f"Checking if user exists: {username}")  # Debugging
            result = self.fetchone(query, (username,))
            print(f"User exists result: {result}")  # Debugging
            return User(id=result[0], username=result[1], password_hash=result[2]) if result else None
        except Exception as e:
            print(f"Error checking user existence: {e}")  # Debugging
        return None

    def find_by_id(self, user_id):
        """
        Finds a user by their ID.
        Returns a User object or None if no match is found.
        """
        query = '''
            SELECT id, username, password_hash
            FROM users
            WHERE id = ?
        '''
        try:
            print(f"Finding user by ID: {user_id}")  # Debugging
            result = self.fetchone(query, (user_id,))
            print(f"Find by ID result: {result}")  # Debugging
            if result:
                return User(id=result[0], username=result[1], password_hash=result[2])
        except Exception as e:
            print(f"Error finding user by ID: {e}")  # Debugging
        return None

