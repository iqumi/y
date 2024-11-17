from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


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
