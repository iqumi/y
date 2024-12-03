from pydantic import UUID4
from typing import AsyncIterator

from database.repositories import chats_repositories
from database.models.chats_models import Chat, GroupChatUser, Chatname


class ChatService:
    """
    Определяет бизнес логику,
    абстрагирует работу с чатами
    """
    names = chats_repositories.ChatnameRepository()
    groups = chats_repositories.GroupChatUserRepository()
    private = chats_repositories.PrivateChatRepository()
    chats = chats_repositories.ChatRepository()

    @classmethod
    async def get_user_chats(
        cls,
        user_id: UUID4
    ) -> list[Chat]:
        """
        Получить все чаты и беседы пользователя по user_id
        >>> await ChatService.get_user_chats(user_id)
        """
        l = list()
        async for chat in cls.chats.get(user_id):
            l.append(chat)
        return l

    @classmethod
    async def create_private_chat(
        cls,
        sender_id: UUID4,
        receiver_id: UUID4,
        message: str,
        sender_name: str,
        receiver_name: str
    ) -> Chat:
        """Создать новый приватный чат"""
        if sender_id > receiver_id:
            sender_id, receiver_id = receiver_id, sender_id

        m = cls.private.model(user1_id=sender_id, user2_id=receiver_id)
        private = await cls.private.save(m)

        last_message = f"{sender_name}: {message}"

        await cls.chats.save(cls.chats.model(
            user_id=sender_id,
            chat_id=private.chat_id,
            last_message=last_message,
            name=receiver_name,
            is_private=True))

        return await cls.chats.save(cls.chats.model(
            user_id=receiver_id,
            chat_id=private.chat_id,
            last_message=last_message,
            name=sender_name,
            is_private=True))

    @classmethod
    async def create_group_chat(
        cls,
        user_id: UUID4,
        chatname: str,
        description: str,
        name: str,
    ) -> GroupChatUser:
        """Создать новую беседу"""
        await cls.names.save(Chatname(chatname))
        group = await cls.groups.save(
            cls.groups.model(
                user_id=user_id,
                description=description,
                name=name,
                nickname="",
                is_admin=True))
        await cls.chats.save(
            cls.chats.model(
                user_id=user_id,
                chat_id=group.chat_id,
                last_message="Чат только что создан",
                name=name,
                is_private=False))
        return group

    def add_user(self):
        pass
