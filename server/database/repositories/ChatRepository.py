from typing import AsyncIterator
from pydantic import UUID4

from database.queries import QUERIES
from database.models import Chat
from . import CassandraRepository


class ChatRepository:
    """Collection of user chats"""
    model = Chat
    repository = CassandraRepository(
        QUERIES["chats"], model)

    async def get(
        self, user_id: UUID4
    ) -> AsyncIterator[model]:
        async for user in self.repository.get(user_id):
            yield user

    async def find(
        self,
        user1_id: UUID4,
        user2_id: UUID4
    ) -> model:
        return await self.repository.find(user1_id, user2_id)

    async def update(
        self,
        field: str,
        user1_id: UUID4,
        chat_id: UUID4,
        user2_id: UUID4 | None = None
    ) -> bool:
        users = [user1_id]
        if user2_id is not None:
            users.append(user2_id)
        return await self.repository.update(
            field=field, users=users, chat_id=chat_id)

    async def save(self, model: model) -> model:
        await self.repository.save(model.__dict__)
        return model
