from app.domains.repositories.base_repository import BaseRepository
from app.domains.value_objects.review import Review

class ReviewRepository(BaseRepository):
    def create_review(self, user_id, username, station_id, rating, comment):
        print("review added")
        """
        Creates a new review in the database with the username.
        """
        query = '''
            INSERT INTO reviews (user_id, username, station_id, rating, comment)
            VALUES (?, ?, ?, ?, ?)
        '''
        self.execute(query, (user_id, username, station_id, rating, comment))

    def get_reviews_by_station(self, station_id):
        """
        Fetches all reviews for a specific station.
        Returns a list of Review objects.
        """
        query = '''
            SELECT id, user_id, station_id, rating, comment
            FROM reviews
            WHERE station_id = ?
        '''
        results = self.fetchall(query, (station_id,))
        return [
            Review(id=row[0], user_id=row[1], station_id=row[2], rating=row[3], comment=row[4])
            for row in results
        ]

    def get_review_by_id(self, review_id):
        """
        Fetches a specific review by its ID.
        Returns a Review object or None if not found.
        """
        query = '''
            SELECT id, user_id, station_id, rating, comment
            FROM reviews
            WHERE id = ?
        '''
        result = self.fetchone(query, (review_id,))
        if result:
            return Review(id=result[0], user_id=result[1], station_id=result[2], rating=result[3], comment=result[4])
        return None

    def delete_review(self, review_id):
        """
        Deletes a review by its ID.
        """
        query = '''
            DELETE FROM reviews
            WHERE id = ?
        '''
        self.execute(query, (review_id,))

    def get_reviews_by_username(self, username):
        print("username:", username)
        """
        Fetches all reviews made by a specific user based on username.
        Returns a list of dictionaries with station name, rating, and comments.
        """
        query = '''
            SELECT *
            FROM reviews r
            WHERE r.username = ?
        '''
        results = self.fetchall(query, (username,))
        print("rseults:", results)
        return [
            {   "review_id": row[0],
                "station_id": row[2],
                "station_ranking": row[3],
                "comment": row[4]
            }
            for row in results
        ]

    def delete_review_by_id(self, review_id):
        """
        Deletes a review by its ID from the database.
        """
        query = '''
            DELETE FROM reviews
            WHERE id = ?
        '''
        self.execute(query, (review_id,))

    def update_review(self, review_id, station_id, rating, comment):
        """
        Updates an existing review in the database.
        """
        query = '''
            UPDATE reviews
            SET station_id = ?, rating = ?, comment = ?
            WHERE id = ?
        '''
        self.execute(query, (station_id, rating, comment, review_id))


