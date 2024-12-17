from database.queries import QUERIES
from database.models import Tag
from . import CassandraRepository


class TagRepository:
    """Collection of users by username"""
    model = Tag
    queries = QUERIES["tags"]
    repository = CassandraRepository(queries, model)

    async def find(self, username: str) -> model:
        return await self.repository.find(username)

    async def save(self, model: model) -> model:
        self.repository.validate_starts_with(model.tag)
        await self.repository.save(model.__dict__)
        return model
