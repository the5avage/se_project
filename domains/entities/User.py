from dataclasses import dataclass, field
from typing import List, Optional
from uuid import uuid4
import bcrypt
from domains.events.charging_station_searched import ChargingStationSearched
from domains.events.charging_station_selected import ChargingStationSelected
from domains.events.review_added import ReviewAdded
from domains.entities.review import Review

@dataclass
class User:
    user_id: str = field(default_factory=lambda: str(uuid4()))
    name: str
    email: str
    password_hash: bytes = field(default=b"", repr=False)  # Store the hashed password
    events: List = field(default_factory=list)

    def set_password(self, password: str):
        """Hash and set the password."""
        if not password:
            raise ValueError("Password cannot be empty")
        self.password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def check_password(self, password: str) -> bool:
        """Verify the password against the stored hash."""
        return bcrypt.checkpw(password.encode("utf-8"), self.password_hash)

    def search_charging_station(self, search_query: str):
        event = ChargingStationSearched(user_id=self.user_id, search_query=search_query)
        self.events.append(event)

    def select_charging_station(self, station_id: str):
        event = ChargingStationSelected(user_id=self.user_id, station_id=station_id)
        self.events.append(event)

    def add_review(self, station_id: str, rating: float, comment: Optional[str] = None):
        review = Review(rating=rating, comment=comment)
        event = ReviewAdded(user_id=self.user_id, station_id=station_id, review=review)
        self.events.append(event)