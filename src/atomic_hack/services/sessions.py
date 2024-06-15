from datetime import datetime
from functools import lru_cache
from uuid import UUID, uuid4

import jinja2

from atomic_hack.entities import chat
from atomic_hack.repositories import pg_chat
from atomic_hack.settings import settings


@lru_cache(maxsize=8)
def _load_template(template_name: str) -> jinja2.Template:
    path_to_template = settings.templates_path + '/' + template_name
    with open(path_to_template, 'r') as f:
        return jinja2.Template(f.read())


def _to_from_user_message(text: str) -> str:
    message_template = _load_template('message.jinja')
    return message_template.render(
        justify_content='flex-end',
        border_radius='15px 15px 0 15px',
        background_color='#88c',
        caption=text,
    )


def _to_from_support_message(text: str) -> str:
    message_template = _load_template('message.jinja')
    return message_template.render(
        justify_content='flex-start',
        border_radius='15px 15px 15px 0',
        background_color='#888',
        caption=text,
    )


def _to_message(text: str, sender: chat.MessageSender) -> str:
    sender2func = {
        chat.MessageSender.from_user: _to_from_user_message,
        chat.MessageSender.from_support: _to_from_support_message,
    }
    return sender2func[sender](text)


async def load_messages_by_id(session_id: UUID) -> str:
    messages: list[chat.ChatSession] = pg_chat.get_session_by_id(session_id)

    if len(messages) == 0:
        greeting_message = 'Привет! Ко мне можно обращаться со всеми вопросами!)'
        pg_chat.insert_message(greeting_message, session_id, sender=chat.MessageSender.from_support)
        messages.append(
            chat.ChatSession(
                session_id=session_id,
                messaage_id=uuid4(),  # placeholder
                sender=chat.MessageSender.from_support,
                message=greeting_message,
                messages_dttm=datetime.now(),  # placeholder
                meta={},
            )
        )

    # добавляем лоадер, если надо
    loader: str = ''
    if messages[-1].sender == chat.MessageSender.from_user:
        loader = '\n' + _load_template('loading.jinja').render()

    return '\n'.join(
        [
            _to_message(msg.message, msg.sender)
            for msg in messages
        ]
    ) + loader


async def load_session_by_id(session_id: UUID | None) -> str:
    session_id: UUID = session_id or uuid4()
    messages = await load_messages_by_id(session_id)

    main = _load_template('main.html')
    return main.render(
        messages=messages,
        session_id=session_id,
    )
