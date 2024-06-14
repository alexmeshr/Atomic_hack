from functools import lru_cache
from uuid import UUID

import jinja2

from atomic_hack.entities import chat
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


async def load_session_by_id(session_id: UUID | None) -> str:
    session_messages = [
        _to_message('У меня нихрена не работает!', chat.MessageSender.from_user),
        _to_message('У нас всё работает!', chat.MessageSender.from_support),
    ]

    main = _load_template('main.html')
    return main.render(messages='\n'.join(session_messages))
