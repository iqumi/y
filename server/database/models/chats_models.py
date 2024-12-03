from dataclasses import dataclass, field
from pydantic import UUID4
from uuid import uuid4

from .base_model import Model


@dataclass
class Chatname(Model):
    chatname: str
    chat_id: UUID4 = field(default_factory=uuid4)
    __already_exist__ = "Беседа с таким адресом уже существует"
    __unknown__ = "Такой беседы не существует"


@dataclass
class GroupChatUser(Model):
    """
    Represents user in group chat
    and group chat info
    """
    user_id: UUID4
    description: str
    name: str
    nickname: str
    is_admin: bool
    chat_id: UUID4 = field(default_factory=uuid4)
    __already_exist__ = "Уже состоит в беседе"
    __unknown__ = "Чата с таким ID не существует"


@dataclass
class PrivateChat(Model):
    user1_id: UUID4
    user2_id: UUID4
    chat_id: UUID4 = field(default_factory=uuid4)
    __already_exist__ = "Чат с пользователем уже существует"
    __unknown__ = "Неизвестный чат"


@dataclass
class Chat(Model):
    """
    Represents private and group chat
    """
    user_id: UUID4
    chat_id: UUID4
    last_message: str
    name: str
    is_private: bool
    __update_error__ = "Не удалось обновить чат"
    __already_exist__ = "Чат уже существует"
    __unknown__ = "У пользователя нет чатов"
