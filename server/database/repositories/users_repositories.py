from pydantic import UUID4

from .base_repository import CassandraRepository
from database.queries import QUERIES
from database.models.users_models import Username, User


class UsernameRepository:
    """Collection of users by username"""
    model = Username
    queries = QUERIES["users_by_name"]
    repository = CassandraRepository(queries, model)

    async def find(self, username: str) -> model:
        return await self.repository.find(username)

    async def save(self, model: model) -> model:
        self.repository.validate_starts_with(model.username)
        await self.repository.save(model.__dict__)
        return model


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
