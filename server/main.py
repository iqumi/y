from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

from database import lifespan  # для конекта к бд
from services import UserService, ChatService, MessageService

app = FastAPI(lifespan=lifespan)


class User:
    username: str
    name: str


usernames = list()


@app.post("/username/")
async def check_username(username: str):
    if username in usernames:
        return False
    usernames.append(username)
    return True


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        chats = await ChatService.get_user_chats(user_id)
        if data == "get_chats":
            await websocket.send_text(chats)