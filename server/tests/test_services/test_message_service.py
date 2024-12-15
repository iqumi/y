import pytest
from datetime import datetime

from services.MessageService import MessageService


class TestMessageService:

    def __init__(self):
        date = datetime.now()
        self.year = date.year
        self.month = date.month

    @pytest.mark.asyncio
    async def test_message_saves_and_returns(self, messages, john_chats):
        """Messages saves and returns for specific chat"""
        chat_id = john_chats[0].chat_id
        async for msg in MessageService.get_chat_messages(chat_id, self.year, self.month):
            assert msg.chat_id == chat_id

    @pytest.mark.asyncio
    async def test_user_message_deletes(self, bill_chat, send_message):
        """Message deletes"""
        chat_id = bill_chat.chat_id
        msg = await send_message(chat_id, bill_chat.user_id, "sample text")
        result = await MessageService.delete_message(
            chat_id,
            msg.created_at,
            msg.message_id)

        assert result == True
        async for msg in MessageService.get_chat_messages(chat_id, self.year, self.month):
            assert False

    @pytest.mark.asyncio
    async def test_unread_messages(self, messages, john_chats):
        """Messages saves to unread, returns then and removes"""
        receiver = john_chats[0].user_chat_id
        msg = messages[0]

        await MessageService.save_to_unread(receiver, msg)
        async for i in MessageService.get_user_unread_messages(receiver):
            assert i.message_id == msg.message_id

        async for i in MessageService.get_user_unread_messages(receiver):
            assert False
