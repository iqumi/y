from dataclasses import dataclass
from pydantic import UUID4

from . import Model


@dataclass
class GroupChat(Model):
    """
    Represents user in group chat
    and group chat info
    """
    chat_id: UUID4
    user_id: UUID4
    description: str
    name: str
    nickname: str
    is_admin: bool
    __already_exist__ = "Уже состоит в беседе"
    __unknown__ = "Чата с таким ID не существует"
