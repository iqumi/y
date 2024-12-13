from typing import AsyncIterator
from pydantic import UUID4

from database.queries import QUERIES
from database.models import UnreadMessage
from . import CassandraRepository


class UnreadMessageRepository:
    """Collection of user unread messages"""
    model = UnreadMessage
    repository = CassandraRepository(
        QUERIES["unread_messages"], model)

    async def get(self, user_id: UUID4) -> AsyncIterator[model]:
        async for msg in self.repository.get(user_id):
            yield msg

    async def save(self, model: model) -> model:
        await self.repository.save(model.__dict__)
        return model

    async def delete(self, chat_id: UUID4, message_id: UUID4) -> bool:
        return await self.repository.delete(
            chat_id=chat_id, message_id=message_id)
