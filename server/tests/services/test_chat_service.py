import pytest

from services.ChatService import ChatService
from schemas import api


class TestChatService:

    @pytest.mark.asyncio
    async def test_user_gets_only_his_chats(self, chats):
        """User gets only his chats"""
        user_id = chats["john"]["user"].user_id
        found = await ChatService.get_user_chats(user_id)

        private = chats["john"]["chats"]["private"]
        group = chats["john"]["chats"]["group"]
        if group.user_chat_id > private.user_chat_id:
            private, group = group, private

        assert [private, group] == found

    @pytest.mark.asyncio
    async def test_names_last_messages_specified(self, chats):
        """Receiver name and chat's last message is being added"""
        group = chats["john"]["chats"]["group"]
        private = chats["john"]["chats"]["private"]
        jack = chats["jack"]["user"]
        assert group == api.Chat(**{
            "user_id": group.user_id,
            "user_chat_id": group.chat_id,
            "chat_id": group.chat_id,
            "name": group.name,
            "last_message": "Беседа только что создана"})
        assert private == api.Chat(**{
            "user_id": private.user_id,
            "user_chat_id": private.user_chat_id,
            "chat_id": private.chat_id,
            "name": jack.name,
            "last_message": None})
