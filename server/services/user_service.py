from database.repositories import users_repositories
from database.models.users_models import User, Username


class UserService:
    usernames = users_repositories.UsernameRepository()
    user = users_repositories.UserRepository()

    @classmethod
    async def find(cls, username: str) -> Username:
        """
        Поиск пользователя по username
        >>> await UserService.find(username="@john")
        """
        return await cls.usernames.find(username)

    @classmethod
    async def save(cls, username: str, name: str, bio: str = "") -> User:
        """
        Сохранить нового пользователя
        >>> await UserService.save("@axaxax", "John")
        """
        # TODO: в batch никак не закинуть, нужен ли он
        u = await cls.usernames.save(Username(username))
        user = await cls.user.save(User(
            user_id=u.user_id,
            name=name,
            bio=bio))
        return user
