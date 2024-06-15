from enum import StrEnum

from pydantic import BaseModel


class MessageRole(StrEnum):
    assistant = 'assistant'
    system = 'system'
    user = 'user'
