from uuid import UUID

from pydantic import BaseModel, Field


class PingResponse(BaseModel):
    message: str = Field(description='ответ на /ping', default='pong')


class PostSendMessageRequest(BaseModel):
    message: str = Field(description='сообщение тех-поддержке')
    session_id: UUID | None = Field(description='сессия-общение с тех-поддержкой', default=None)
