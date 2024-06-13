from typing import Any
from uuid import UUID

from atomic_hack.deps import get_pg_cursor
from atomic_hack.entities.chat import ChatSession


def get_session_by_id(session_id: UUID) -> list[ChatSession]:
    with get_pg_cursor() as cursor:
        cursor.execute(
            '''
            select
                 session_id
                ,message_id
                ,sender
                ,message
                ,message_dttm
                ,meta
            from
                support_chat
            where
                session_id=%s
            ''',
            (str(session_id),)
        )
        # вообще хз, что тут за тип
        data: list[tuple[Any]] = cursor.fetchall()

    return ChatSession.from_sequence2(data)

