# handle common database operations like creating connections, committing, and rolling back transactions
import sqlite3

class BaseRepository:
    def __init__(self, db_path='db.sqlite3'):
        self.db_path = db_path

    def connect(self):
        """Establish a database connection."""
        return sqlite3.connect(self.db_path)

    def execute(self, query, params=None):
        """Execute a query with optional parameters."""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def fetchall(self, query, params=None):
        """Fetch all results from a query."""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        finally:
            conn.close()

    def fetchone(self, query, params=None):
        """Fetch a single result from a query."""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchone()
        finally:
            conn.close()
