from uuid import UUID, uuid4


from atomic_hack.entities import chat
from atomic_hack.settings import settings


async def save_user_message(message: str, session_id: UUID):
    pass