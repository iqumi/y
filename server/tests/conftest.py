import pytest
import redis
from cassandra.query import SimpleStatement

from database import Cassandra, Valkey
from database.queries import QUERIES
from config import CACHE


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Setup database and redis before all tests"""
    Valkey.session = redis.Redis(**CACHE, decode_responses=True)
    with Cassandra():
        yield


@pytest.fixture(autouse=True)
def clean_database():
    """Clean database after each test"""
    for table in QUERIES.keys():
        Cassandra.session.execute(SimpleStatement(f"TRUNCATE {table};"))
    Valkey.session.flushdb()
