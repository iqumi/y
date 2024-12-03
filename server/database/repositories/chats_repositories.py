from typing import AsyncIterator
from pydantic import UUID4

from .base_repository import CassandraRepository
from database.queries import QUERIES
from ..models.chats_models import Chatname, PrivateChat, GroupChatUser, Chat


class ChatnameRepository:
    """Collection of group chats by chatname"""
    model = Chatname
    repository = CassandraRepository(
        QUERIES["chats_by_name"], model)

    async def find(self, chatname: str) -> model:
        return await self.repository.find(chatname)

    async def save(self, model: model) -> model:
        self.repository.validate_starts_with(model.chatname, "Имя беседы")
        await self.repository.save(model.__dict__)
        return model


class GroupChatUserRepository:
    """Collection of group chats and their users by chat_id"""
    model = GroupChatUser
    repository = CassandraRepository(
        QUERIES["group_chat_users"], model)

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


class PrivateChatRepository:
    """Collection of private chats"""
    model = PrivateChat
    repository = CassandraRepository(
        QUERIES["private_chats"],model)

    async def find(self, user1_id: UUID4, user2_id: UUID4) -> model:
        return await self.repository.find(user1_id, user2_id)

    async def save(self, model: model) -> model:
        await self.repository.save(model.__dict__)
        return model


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
