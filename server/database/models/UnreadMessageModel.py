from datetime import datetime
from dataclasses import dataclass
from pydantic import UUID4

from . import Model


@dataclass
class UnreadMessage(Model):
    user_id: UUID4
    chat_id: UUID4
    message_id: UUID4
    created_at: datetime
    sender: UUID4
    text: str
    __delete_error__ = "Сообщение не было удалено"
    __unknown__ = "Такого сообщения не существует"
