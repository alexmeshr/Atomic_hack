from typing import Annotated
from uuid import UUID

from fastapi import FastAPI, Form, Query
from fastapi.responses import HTMLResponse

from atomic_hack.entities.web import PingResponse
from atomic_hack.services import chat, sessions

app = FastAPI()


@app.get('/ping')
async def ping() -> PingResponse:
    return PingResponse()


@app.get('/chat')
async def get_chat(session_id: UUID | None = None) -> HTMLResponse:
    data = await sessions.load_session_by_id(session_id)
    return HTMLResponse(content=data, status_code=200)


@app.get('/messages')
async def get_messages(session_id: UUID) -> HTMLResponse:
    data = await sessions.load_messages_by_id(session_id)
    return HTMLResponse(content=data, status_code=200)



@app.post('/send-message')
async def post_send_message(
    message: str = Form(alias='input-area'),
    session_id: UUID = Form(...),
) -> HTMLResponse:
    await chat.save_user_message(message, session_id)
    return HTMLResponse(content='ok', status_code=200)
