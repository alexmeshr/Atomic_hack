from uuid import UUID

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from atomic_hack.entities.web import PingResponse, PostSendMessageRequest
from atomic_hack.services import sessions

app = FastAPI()


@app.get('/ping')
async def ping() -> PingResponse:
    return PingResponse()


@app.get('/chat')
async def get_chat(session_id: UUID | None = None) -> HTMLResponse:
    data = await sessions.load_session_by_id(session_id)
    return HTMLResponse(content=data, status_code=200)


@app.post('/send-message')
async def post_send_message(request: PostSendMessageRequest) -> HTMLResponse:
    print(request)
