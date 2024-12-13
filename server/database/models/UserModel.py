from dataclasses import dataclass
from pydantic import UUID4

from . import Model


@dataclass
class User(Model):
    user_id: UUID4
    name: str
    bio: str | None = None
    email: str | None = None
    __already_exist__ = "Пользователь с таким ID уже существует"
    __unknown__ = "Пользователя с таким ID не существует"
