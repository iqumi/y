import pytest

from database.models import Chat, User
from services.ChatService import ChatService
from schemas import api


class TestChatService:

    @pytest.mark.asyncio
    async def test_user_gets_only_his_chats(
        self,
        bill_chat: Chat,
        john_chats: list[Chat],
        users: dict[str, User]
    ) -> None:
        """User gets only his chats"""
        found = await ChatService.get_user_chats(users["john"].user_id)
        chats = sorted(john_chats, key=lambda chat: chat.user_chat_id, reverse=True)
        assert chats == found

    @pytest.mark.asyncio
    async def test_names_last_messages_specified(
        self,
        bill_chat: Chat,
        users: dict[str, User]
    ) -> None:
        """Receiver name and chat's last message is being added"""
        assert bill_chat == api.Chat(**{
            "user_id": users["bill"].user_id,
            "user_chat_id": users["mike"].user_id,
            "chat_id": bill_chat.chat_id,
            "name": users["mike"].name,
            "last_message": None})
