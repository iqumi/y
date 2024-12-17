from dataclasses import dataclass
from pydantic import UUID4
from typing import Optional

# Schema for api responses


@dataclass
class Chat:
    user_id: UUID4
    user_chat_id: UUID4
    chat_id: UUID4
    last_message: Optional[str] = None
    name: Optional[str] = None
