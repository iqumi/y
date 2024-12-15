import pytest

from services.UserService import UserService
from database.models import Tag


class TestUserService:

    @pytest.mark.asyncio
    async def test_user_saves_and_findes(self, users):
        """User is being saved and searched"""
        user = users["john"]
        found = await UserService.get_user("@john")
        assert user.user_id == found.user_id

    @pytest.mark.asyncio
    async def test_unknown_username_not_findes(self):
        """User that doesn't exist should not be found"""
        with pytest.raises(Exception) as e:
            await UserService.get_user("@unknownuser")
        assert str(e.value) == Tag.__unknown__

    @pytest.mark.asyncio
    async def test_same_user_not_saves(self, create_user):
        """User with same username should not be saved"""
        before = await create_user("@john", "John")
        with pytest.raises(Exception) as e:
            await create_user("@john", "Jim")

        after = await UserService.get_user("@john")
        assert str(e.value) == Tag.__already_exist__
        assert before.user_id == after.user_id

    @pytest.mark.asyncio
    async def test_username_starts_with(self, create_user):
        """Username without @ character should not be saved"""
        with pytest.raises(Exception) as e:
            await create_user("john", "John")
        assert str(e.value) == Tag.__starts_with__
