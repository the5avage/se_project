
class User:
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"
