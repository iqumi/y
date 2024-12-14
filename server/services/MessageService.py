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
        year_month: str = datetime.now().strftime("%Y-%m")
    ) -> list[Message]:
        """Получить все сообщения в чате по chat_id"""
        l = []
        async for chat in cls.messages.get(chat_id, year_month):
            l.append(chat)
        return l

    @classmethod
    async def send_message(
        cls,
        chat_id: UUID4,
        receiver: UUID4,
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
        message_id: UUID4
    ) -> None:
        pass

    @classmethod
    async def get_user_unread_messages(
        cls, user_id: UUID4
    ) -> AsyncIterator[UnreadMessage]:
        """Получить все непрочитанные сообщения пользователя"""
        async for chat in cls.unread_messages.get(user_id):
            yield chat

    @classmethod
    async def _remove_from_unread(cls):
        pass

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
