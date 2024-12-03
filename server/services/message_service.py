from datetime import datetime
from typing import AsyncIterator
from pydantic import UUID4

from database.repositories import messages_repositories
from database.models.messages_models import Message, UnreadMessage


class MessageService:
    """
    Абстрагирует работу с сообщениями
    """
    messages = messages_repositories.MessageRepository()
    unread_messages = messages_repositories.UnreadMessageRepository()

    @classmethod
    async def get_chat_messages(
        cls,
        chat_id: UUID4,
        year_month: str = datetime.now().strftime("%Y-%m")
    ) -> AsyncIterator[Message]:
        """Получить все сообщения в чате по chat_id"""
        async for chat in cls.messages.get(chat_id, year_month):
            yield chat

    @classmethod
    async def get_user_unread_messages(
        cls, user_id: UUID4
    ) -> AsyncIterator[UnreadMessage]:
        """Получить все непрочитанные сообщения пользователя"""
        async for chat in cls.unread_messages.get(user_id):
            yield chat

    @classmethod
    async def save_message_to_unread(
        cls, message: Message
    ) -> UnreadMessage:
        """Сохранить сообщение в непрочитанные"""
        return await cls.unread_messages.save(UnreadMessage(
            user_id=message.receiver,
            chat_id=message.chat_id,
            message_id=message.message_id,
            created_at=message.created_at,
            sender=message.sender,
            text=message.text
        ))

    @classmethod
    async def save(
        cls,
        chat_id: UUID4,
        receiver: UUID4,
        sender: UUID4,
        text: str,
        data: str | None = None,
    ) -> Message:
        """Сохранить новое сообщение"""
        msg = Message(chat_id, receiver, sender, text, data)
        return await cls.messages.save(msg)
