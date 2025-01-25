class Review:
    def __init__(self, id, user_id, username, station_id, rating, comment):
        self.id = id
        self.user_id = user_id
        self.username = username
        self.station_id = station_id
        self.rating = rating
        self.comment = comment

    def __repr__(self):
        return f"<Review by User {self.username} for Station {self.station_id}>"
