import click
import uvicorn

from atomic_hack.web import app


@click.group
def cli():
    pass


@cli.command
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=8888)
def run_server(host: str, port: int):
    uvicorn.run(app, host=host, port=port)


@cli.command
def do():
    from uuid import uuid4
    from atomic_hack.repositories import pg_chat

    pg_chat.get_session_by_id(uuid4())
