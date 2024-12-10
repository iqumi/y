import pytest

from services.chat_service import ChatService


class TestChatService:
    @pytest.mark.asyncio
    async def test_user_gets_only_his_chats(self, chats):
        """User gets only his chats"""
        found = await ChatService.get_user_chats(chats["john"]["id"])
        assert len(found) == 2
        assert len(chats["john"]["chats"]) == 2
        assert chats["john"]["chats"][0] in found
        assert chats["john"]["chats"][1] in found
