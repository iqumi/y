from datetime import datetime
from typing import AsyncIterator
from pydantic import UUID4

from database.repositories import MessageRepository, UnreadMessageRepository
from database.models import Message, UnreadMessage
from database import Valkey


class MessageService:
    """
    Абстрагирует работу с сообщениями
    """
    messages = MessageRepository()
    unread_messages = UnreadMessageRepository()

    @classmethod
    async def get_chat_messages(
        cls,
        chat_id: UUID4,
        year: int,
        month: int
    ) -> AsyncIterator[Message]:
        """Получить все сообщения в чате по chat_id"""
        year_month = datetime(year, month, 1).strftime("%Y-%m")
        async for chat in cls.messages.get(chat_id, year_month):
            yield chat

    @classmethod
    async def send_message(
        cls,
        chat_id: UUID4,
        sender: UUID4,
        text: str,
        data: str | None = None,
    ) -> Message:
        """Сохранить новое сообщение"""
        msg = Message(chat_id, sender, text, data)
        Valkey.session.set(f"chat:{chat_id}:message", text)
        return await cls.messages.save(msg)

    @classmethod
    async def delete_message(
        cls,
        chat_id: UUID4,
        created_at: datetime,
        message_id: UUID4,
    ) -> bool:
        year_month = created_at.strftime("%Y-%m")
        return await cls.messages.delete(
            chat_id, year_month, message_id)

    @classmethod
    async def get_user_unread_messages(
        cls,
        user_id: UUID4
    ) -> AsyncIterator[UnreadMessage]:
        """Получить все непрочитанные сообщения пользователя"""
        async for chat in cls.unread_messages.get(user_id):
            yield chat
        await cls._remove_from_unread(user_id)

    @classmethod
    async def save_to_unread(
        cls,
        receiver: UUID4,
        message: Message
    ) -> UnreadMessage:
        """Сохранить сообщение в непрочитанные"""
        return await cls.unread_messages.save(UnreadMessage(
            user_id=receiver,
            chat_id=message.chat_id,
            message_id=message.message_id,
            created_at=message.created_at,
            sender=message.sender,
            text=message.text
        ))

    @classmethod
    async def _remove_from_unread(cls, user_id: UUID4) -> bool:
        """
        Из непрочитанных удаляем все,
        фронт разберется как это отображать
        счетчиски и прочее
        """
        return await cls.unread_messages.delete(user_id=user_id)
