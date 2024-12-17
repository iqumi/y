from pydantic import UUID4

from database.repositories import TagRepository, UserRepository
from database.models import User, Tag
from database import Valkey


class UserService:
    usernames = TagRepository()
    user = UserRepository()

    @classmethod
    async def get_user(cls, username: str) -> User:
        """
        Поиск пользователя по его username
        >>> await UserService.get_user(username="@john")
        """
        u = await cls.usernames.find(username)
        return await cls.user.find(u.id)

    @classmethod
    async def change_name(cls, user_id: UUID4, username: str) -> None:
        pass

    @classmethod
    async def create_user(
        cls,
        username: str,
        name: str,
        email: str = "",
        bio: str = ""
    ) -> User:
        """
        Сохранить нового пользователя
        >>> await UserService.create_user("@axaxax", "John")
        """
        u = await cls.usernames.save(Tag(username))
        user = await cls.user.save(User(
            user_id=u.id,
            name=name,
            email=email,
            bio=bio))
        Valkey.session.set(f"user:{u.id}:name", name)
        return user
