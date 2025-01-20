from dataclasses import dataclass, field
from typing import List, Optional
from uuid import uuid4
import bcrypt
from domains.events.chargingStationSearched import ChargingStationSearched
from domains.events.chargingStationSelected import ChargingStationSelected
from domains.events.reviewAdded import ReviewAdded
from domains.value_objects.Review import Review


@dataclass
class User:
    name: str  # Non-default argument
    email: str  # Non-default argument
    user_id: str = field(default_factory=lambda: str(uuid4()))  # Default argument
    password_hash: bytes = field(default=b"", repr=False)  # Default argument
    events: List = field(default_factory=list)  # Default argument

    def set_password(self, password: str):
        """Hash and set the password."""
        if not password:
            raise ValueError("Password cannot be empty")
        self.password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def check_password(self, password: str) -> bool:
        """Verify the password against the stored hash."""
        return bcrypt.checkpw(password.encode("utf-8"), self.password_hash)

    def add_review(self, station_id: str, rating: float, comment: str = None):
        from domains.value_objects.Review import Review
        from domains.events.reviewAdded import ReviewAdded
        review = Review(rating=rating, comment=comment)
        event = ReviewAdded(user_id=self.user_id, station_id=station_id, review=review)
        self.events.append(event)