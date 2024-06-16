import os

import click
import uvicorn

from atomic_hack.services import pipeline, pdf_loader
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
def llm_pipeline():
    # pipeline.summarization_example()
    pipeline.main_pipeline()


@cli.command
@click.option('--path', default=None)
def upload_instructions(path: str):
    assert isinstance(path, str)

    print('running...')
    pdf_loader.process_folder_with_pdfs(path)
    print('DONE! DONE! DONE! DONE! DONE! DONE! DONE! DONE! DONE! DONE!')
    print("pds'f are loaded!")
    print('DONE! DONE! DONE! DONE! DONE! DONE! DONE! DONE! DONE! DONE!')


@cli.command
def do():
    pass
