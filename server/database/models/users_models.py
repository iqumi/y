from dataclasses import dataclass, field
from pydantic import UUID4
from uuid import uuid4

from .base_model import Model


@dataclass
class Username(Model):
    username: str
    user_id: UUID4 = field(default_factory=uuid4)
    __already_exist__ = "Пользователь с таким username уже существует"
    __unknown__ = "Такого пользователя не существует"


@dataclass
class User(Model):
    name: str
    bio: str
    user_id: UUID4 = field(default_factory=uuid4)
    __already_exist__ = "Пользователь с таким ID уже существует"
    __unknown__ = "Пользователя с таким ID не существует"
