from contextlib import asynccontextmanager

from fastapi import FastAPI
import redis

from config import CACHE
from . import Cassandra


class Valkey:
    session: redis.Redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Will be executed before and after our app"""
    Valkey.session = redis.Redis(**CACHE)
    with Cassandra():
        yield
