import unittest
from domains.entities.user import User
from domains.entities.review import Review
from domains.events.review_added import ReviewAdded

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User(name="John Doe", email="john.doe@example.com")

    def test_set_password(self):
        self.user.set_password("securepassword123")
        self.assertNotEqual(self.user.password_hash, b"")  # Ensure password is hashed

    def test_check_password(self):
        self.user.set_password("securepassword123")
        self.assertTrue(self.user.check_password("securepassword123"))  # Correct password
        self.assertFalse(self.user.check_password("wrongpassword"))  # Incorrect password

    def test_set_empty_password(self):
        with self.assertRaises(ValueError):
            self.user.set_password("")  # Empty password should raise an error

    def test_add_review(self):
        self.user.add_review("station_123", 4.5, "Great station!")
        self.assertEqual(len(self.user.events), 1)
        self.assertIsInstance(self.user.events[0], ReviewAdded)

if __name__ == "__main__":
    unittest.main()