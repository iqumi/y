from typing import AsyncIterator
from pydantic import UUID4

from database.queries import QUERIES
from database.models import GroupChat
from . import CassandraRepository


class GroupChatRepository:
    """Collection of group chats and their users by chat_id"""
    model = GroupChat
    repository = CassandraRepository(
        QUERIES["group_chats"], model)

    async def get(
        self, chat_id: UUID4
    ) -> AsyncIterator[model]:
        async for user in self.repository.get(chat_id):
            yield user

    async def find(self, chat_id: UUID4, user_id: UUID4) -> model:
        return await self.repository.find(chat_id, user_id)

    async def save(self, model: model) -> model:
        await self.repository.save(model.__dict__)
        return model
