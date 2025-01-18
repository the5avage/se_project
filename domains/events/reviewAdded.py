from dataclasses import dataclass
from datetime import datetime
from domains.entities.review import Review  # Import the Review class

@dataclass
class ReviewAdded:
    user_id: str
    station_id: str
    review: Review
    timestamp: datetime = datetime.now()