# # what will be here?
# # - DataStorage class

# class DataStorage:
#     def __init__(self):
#         self.data = {}

#     def get(self, key):
#         return self.data.get(key)

#     def set(self, key, value):
#         self.data[key] = value

#     def delete(self, key):
#         if key in self.data:
#             del self.data[key]

#     def get_all(self):
#         return self.data
    
#     def clear(self):
#         self.data = {}
# # - User class

# from dataclasses import dataclass, field
# from typing import List, Optional
# from uuid import uuid4

# @dataclass
# class User:
#     name: str
#     email: str
#     user_id: str = field(default_factory=lambda: str(uuid4()))
#     password_hash: bytes = field(default=b"", repr=False)
#     events: List = field(default_factory=list)
    
#     def set_password(self, password: str):
#         if not password:
#             raise ValueError("Password cannot be empty")
#         self.password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        
#     def check_password(self, password: str) -> bool:
#         return bcrypt.checkpw(password.encode("utf-8"), self.password_hash)

        
#     def add_review(self, station_id: str, rating: float, comment: str = None):
#         from domains.value_objects.Review import Review
#         from domains.events.reviewAdded import ReviewAdded
#         review = Review(rating=rating, comment=comment)
#         event = ReviewAdded(user_id=self.user_id, station_id=station_id, review=review)
#         self.events.append(event)
        
#     def __eq__(self, other):
#         return self.user_id == other.user_id
# # - Station class
