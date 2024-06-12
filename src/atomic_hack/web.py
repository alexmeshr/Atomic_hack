from fastapi import FastAPI

from atomic_hack.entities.web import PingResponse

app = FastAPI()


@app.get('/ping')
async def ping() -> PingResponse:
    return PingResponse()
