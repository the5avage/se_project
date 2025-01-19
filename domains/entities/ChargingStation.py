class ChargingStation:
    def __init__(self, id, address, capacity, reviews=None):
        self.id = id
        self.address = address  # Address is a value object
        self.capacity = capacity
        self.reviews = reviews or []

    def add_review(self, review):
        self.reviews.append(review)
