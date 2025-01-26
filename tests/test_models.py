from app.domains.repositories.review_repository import ReviewRepository

def test_create_review(client):
    review_repo = ReviewRepository()

    # Add a review
    review_repo.create_review(user_id=1, username="testuser", station_id=1, rating=5, comment="Great station!")
    reviews = review_repo.get_reviews_by_username("testuser")
    
    assert len(reviews) > 0
    assert reviews[0]["comment"] == "Great station!"
