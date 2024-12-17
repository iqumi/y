from dataclasses import dataclass, field
from pydantic import UUID4
from uuid import uuid4

from . import Model


@dataclass
class Chat(Model):
    """
    Represents private and group chat
    """
    user_id: UUID4
    user_chat_id: UUID4
    chat_id: UUID4 = field(default_factory=uuid4)  # gen only for private
    __already_exist__ = "Чат уже существует"
    __unknown__ = "Неизвестный чат"
