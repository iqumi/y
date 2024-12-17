from dataclasses import dataclass, field
from pydantic import UUID4
from uuid import uuid4

from . import Model


@dataclass
class Tag(Model):
    tag: str
    id: UUID4 = field(default_factory=uuid4)
    __starts_with__ = "Тег должен начинаться с символа '@'"
    __already_exist__ = "Тег занят"
    __unknown__ = "Ничего не найдено"
