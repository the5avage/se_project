# app/domain/events/review_events.py

class ReviewEvent:
    """Base class for review-related events."""
    pass


class ReviewAdded(ReviewEvent):
    def __init__(self, user_id, username, station_id, rating, comment):
        self.user_id = user_id
        self.username = username
        self.station_id = station_id
        self.rating = rating
        self.comment = comment

    def __repr__(self):
        return f"<ReviewAdded user_id={self.user_id} username={self.username} station_id={self.station_id}>"


class ReviewPageAccessed(ReviewEvent):
    def __init__(self, user_id=None):
        self.user_id = user_id

    def __repr__(self):
        return f"<ReviewPageAccessed user_id={self.user_id}>"


class UserReviewsAccessed(ReviewEvent):
    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return f"<UserReviewsAccessed username={self.username}>"
