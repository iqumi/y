from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

from database import lifespan  # для конекта к бд
from services import UserService, ChatService, MessageService

from pydantic import UUID4


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
        data = await websocket.receive_json()
        action = data["action"]

        chats = await ChatService.get_user_chats(user_id)
        if action == "get_chats":
            await websocket.send_json(chats)
        
        elif action == "get_messages":
            chat_id = data["chat_id"]
            # список возвращаемых сообщений 
            first_n_messages_to_return = []
            # из генератора достаем сообщения
            async for message in MessageService.get_chat_messages(data["chat_id"]):
                # добавляем сообщение в список
                first_n_messages_to_return.append(message)
                # если в списке 10 сообщений
                if len(first_n_messages_to_return) == 10:
                    # отправляем клиенту
                    await websocket.send_json(first_n_messages_to_return)
                    # список очищаем
                    first_n_messages_to_return = []
                # после цикла если в списке еще остались сообщения
            if len(first_n_messages_to_return) != 0:
                # добейте выживших
                await websocket.send_json(first_n_messages_to_return)
        elif action == "save_message":
            chat_id = data["chat_id"]
            sender_id = data["sender_id"]
            text = data["text"]
            await MessageService.send_message(
                chat_id, 
                sender_id, 
                text)
        elif action == "delete_message":
            chat_id = data["chat_id"]
            created_at = data["created_at"]
            message_id = data["message_id"]
            await MessageService.delete_message(
                chat_id, 
                created_at, 
                message_id)
            await websocket.send_text("OK")        
        elif action == "show_me_unread_messages":
            user_id: UUID4 = data["user_id"]
            messages = []
            async for i in MessageService.get_user_unread_messages(user_id):
                messages.append(i)
            await websocket.send_json(messages)
            