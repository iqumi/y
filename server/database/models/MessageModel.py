from datetime import datetime
from dataclasses import dataclass, field
from pydantic import UUID4
from uuid import uuid4

from . import Model


@dataclass
class Message(Model):
    chat_id: UUID4
    sender: UUID4
    text: str
    data: str | None = None
    year_month: str = datetime.now().strftime("%Y-%m")
    message_id: UUID4 = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    read_at: datetime | None = None
    __delete_error__ = "Сообщение не было удалено"
    __unknown__ = "Такого сообщения не существует"
