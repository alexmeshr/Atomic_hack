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
    print('hello')
