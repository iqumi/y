from typing import AsyncIterator
from pydantic import UUID4

from .base_repository import CassandraRepository
from database.queries import QUERIES
from ..models.messages_models import Message, UnreadMessage


class MessageRepository:
    """Collection of chat messages"""
    model = Message
    repository = CassandraRepository(
        QUERIES["messages"], model)

    async def get(
        self, chat_id: UUID4, year_month: str
    ) -> AsyncIterator[model]:
        async for msg in self.repository.get(chat_id, year_month):
            yield msg

    async def find(
        self,
        chat_id: UUID4,
        year_month: str,
        message_id: UUID4
    ) -> model:
        return await self.repository.find(
            chat_id,
            year_month,
            message_id)

    async def save(self, model: model) -> model:
        await self.repository.save(model.__dict__)
        return model


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
