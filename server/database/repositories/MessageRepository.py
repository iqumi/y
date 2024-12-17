from types import NoneType
from typing import AsyncIterator
from pydantic import UUID4

from database.queries import QUERIES
from database.models import Message
from . import CassandraRepository


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

    async def delete(
        self,
        chat_id: UUID4,
        year_month: str,
        message_id: UUID4
    ) -> bool:
        return await self.repository.delete(
            chat_id=chat_id,
            year_month=year_month,
            message_id=message_id)
