from uuid import UUID

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from atomic_hack.entities.web import PingResponse

app = FastAPI()


@app.get('/ping')
async def ping() -> PingResponse:
    return PingResponse()


@app.get('/chat')
async def get_chat(session_id: UUID | None = None) -> HTMLResponse:
    from os import path
    from atomic_hack.settings import settings
    with open(path.join(settings.templates_path, 'main.html'), 'r') as f:
        data = f.read()
    return HTMLResponse(content=data, status_code=200)
