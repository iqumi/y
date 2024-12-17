from pydantic import UUID4

from database.queries import QUERIES
from database.models import User
from . import CassandraRepository


class UserRepository:
    """Collection of users and their data by user_id"""
    model = User
    queries = QUERIES["users"]
    repository = CassandraRepository(queries, model)

    async def find(self, user_id: UUID4) -> model:
        return await self.repository.find(user_id)

    async def save(self, model: model) -> model:
        await self.repository.save(model.__dict__)
        return model
