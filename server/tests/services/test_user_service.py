import pytest
from cassandra.query import SimpleStatement

from services.user_service import UserService
from database.models import Username
from database import Cassandra


class TestUserService:

    @pytest.mark.asyncio
    async def test_user_saves_and_findes(self, user):
        """User is being saved and searched"""
        user = await user("@john", "John")
        found = await UserService.find(username="@john")
        assert user.user_id == found.user_id

    @pytest.mark.asyncio
    async def test_unknown_username_not_findes(self):
        """User that doesn't exist should not be found"""
        with pytest.raises(Exception) as e:
            await UserService.find("@unknownuser")
        assert str(e.value) == Username.__unknown__

    @pytest.mark.asyncio
    async def test_same_user_not_saves(self, user):
        """User with same username should not be saved"""
        before = await user("@john", "John")
        with pytest.raises(Exception) as e:
            await user("@john", "Jim")

        after = await UserService.find("@john")
        assert str(e.value) == Username.__already_exist__
        assert before.user_id == after.user_id

    @pytest.mark.asyncio
    async def test_username_starts_with(self, user):
        """Username without @ character should not be saved"""
        with pytest.raises(Exception) as e:
            await user("john", "John")
        assert str(e.value) == Username.__starts_with__
