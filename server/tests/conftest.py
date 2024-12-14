import pytest
import redis

from database import Cassandra
from database.lifespan import Valkey
from config import CACHE


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Valkey.session = redis.Redis(**CACHE, decode_responses=True)
    with Cassandra():
        yield
