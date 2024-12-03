from fastapi import FastAPI

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
