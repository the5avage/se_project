from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Review:
    rating: float
    comment: Optional[str] = None

    def __post_init__(self):
        if not (0 <= self.rating <= 5):
            raise ValueError("Rating must be between 0 and 5")