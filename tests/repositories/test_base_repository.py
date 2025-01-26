import pytest
import sqlite3
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.domains.repositories.base_repository import BaseRepository


# Fixture to create a temporary database for testing
@pytest.fixture
def test_db():
    db_path = 'test_db.sqlite3'
    if os.path.exists(db_path):
        os.remove(db_path)
    yield db_path
    if os.path.exists(db_path):
        os.remove(db_path)

@pytest.fixture
def base_repository(test_db):
    return BaseRepository(db_path=test_db)

# Test BaseRepository connection
def test_connect(base_repository):
    conn = base_repository.connect()
    assert isinstance(conn, sqlite3.Connection)
    conn.close()

# Test execute method
def test_execute(base_repository):
    base_repository.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")
    base_repository.execute("INSERT INTO test_table (name) VALUES (?)", ("Test Name",))
    result = base_repository.fetchall("SELECT * FROM test_table")
    assert len(result) == 1
    assert result[0][1] == "Test Name"

# Test fetchall method
def test_fetchall(base_repository):
    base_repository.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")
    base_repository.execute("INSERT INTO test_table (name) VALUES (?)", ("Test Name 1",))
    base_repository.execute("INSERT INTO test_table (name) VALUES (?)", ("Test Name 2",))
    results = base_repository.fetchall("SELECT * FROM test_table")
    assert len(results) == 2
    assert results[0][1] == "Test Name 1"
    assert results[1][1] == "Test Name 2"

# Test fetchone method
def test_fetchone(base_repository):
    base_repository.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")
    base_repository.execute("INSERT INTO test_table (name) VALUES (?)", ("Test Name",))
    result = base_repository.fetchone("SELECT * FROM test_table WHERE name = ?", ("Test Name",))
    assert result is not None
    assert result[1] == "Test Name"

# Test handling of exceptions in execute method
def test_execute_exception(base_repository):
    base_repository.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")
    with pytest.raises(sqlite3.OperationalError):
        base_repository.execute("INSERT INTO test_table (nonexistent_column) VALUES (?)", ("Test",))