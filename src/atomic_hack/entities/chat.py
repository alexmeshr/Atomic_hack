from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4
from typing import Any, Self, Sequence

from pydantic import BaseModel, Field


class MessageSender(StrEnum):
    from_user: str = 'from_user'
    from_support: str = 'from_support'


class ChatSession(BaseModel):
    session_id: UUID = Field(description='айдишник сессии', default_factory=uuid4)
    message_id: UUID = Field(description='айдишник сообщения', default_factory=uuid4)
    sender: MessageSender = Field(description='от кого сообщение')
    message: str = Field(description='само сообщение')
    message_dttm: datetime = Field(description='время получения сообщения', default_factory=datetime.now)
    meta: dict[str, Any] = Field(description='метаинфа', default_factory=dict)

    @classmethod
    def form_sequence(cls, it: Sequence[Any]) -> Self:
        return cls(**{k: v for k, v in zip(cls.__fields__.keys(), it)})


    @classmethod
    def from_sequence2(cls, it2: Sequence[Sequence[Any]]) -> list[Self]:
        # сори, не придумал название лучше
        return [cls.from_iterable(it) for it in it2]
