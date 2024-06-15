from uuid import UUID, uuid4


from atomic_hack.entities.chat import MessageSender
from atomic_hack.repositories import pg_chat
from atomic_hack.settings import settings


async def save_user_message(message: str, session_id: UUID):
    pg_chat.insert_message(message, session_id, MessageSender.from_user)
