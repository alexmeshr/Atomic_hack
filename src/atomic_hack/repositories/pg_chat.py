from typing import Any
from uuid import UUID, uuid4

from atomic_hack.deps import get_pg_cursor
from atomic_hack.entities.chat import ChatSession, MessageSender


def get_session_by_id(session_id: UUID) -> list[ChatSession]:
    with get_pg_cursor() as cursor:
        exe_cursor = cursor.execute(
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
            order by
                message_dttm asc
            ''',
            (str(session_id),)
        )
        # вообще хз, что тут за тип
        data: list[tuple[Any]] = []
        if exe_cursor.rowcount:
            data = cursor.fetchall()

    return ChatSession.from_sequence2(data)


def insert_message(message: str, session_id: UUID, sender: MessageSender):
    with get_pg_cursor() as cursor:
        cursor.execute(
            '''
            insert into support_chat (session_id, message_id, sender, message, message_dttm, meta)
            values (
                 %s  -- session_id
                ,%s  -- message_id
                ,%s  -- sender
                ,%s  -- message
                ,now()  -- message_dttm
                ,'{}'  -- meta
            )
            ''',
            (str(session_id), str(uuid4()), sender, message)
        )


def get_oldest_unprocessed_session() -> list[ChatSession]:
    with get_pg_cursor() as cursor:
        exe_cursor = cursor.execute(
            '''
            with last_messages as (
                select distinct
                     session_id
                    ,first_value(sender) over (partition by session_id order by message_dttm desc) as value
                    ,max(message_dttm) over (partition by session_id) as last_communication
                from
                    support_chat
            )
            ,last_sender as (
                select
                     session_id
                    ,value
                from
                    last_messages
                where
                    value = 'from_user'  -- берем неотвеченные
                order by
                    last_communication asc
                limit 1
            )
            select
                 support_chat.session_id
                ,support_chat.message_id
                ,support_chat.sender
                ,support_chat.message
                ,support_chat.message_dttm
                ,support_chat.meta
            from
                support_chat
                inner join last_sender
                on
                    1=1
                    and support_chat.session_id = last_sender.session_id
            order by
                message_dttm asc
            '''
        )

        # вообще хз, что тут за тип
        data: list[tuple[Any]] = []
        if exe_cursor.rowcount:
            data = cursor.fetchall()

    session = ChatSession.from_sequence2(data)
    if not session:
        return []

    # скипаем первое системное сообщение
    return session[1:]
