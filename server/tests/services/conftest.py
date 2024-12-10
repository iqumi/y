import pytest
from cassandra.query import SimpleStatement

from services import UserService, ChatService, MessageService
from database import models as m
from database import Cassandra


@pytest.fixture
async def user():
    Cassandra.session.execute(SimpleStatement("TRUNCATE users_by_name;"))
    Cassandra.session.execute(SimpleStatement("TRUNCATE users;"))
    async def create(username: str, name: str) -> m.User:
        return await UserService.save(username, name)
    return create


@pytest.fixture
async def chats(user):
    Cassandra.session.execute(SimpleStatement("TRUNCATE chats_by_name;"))
    Cassandra.session.execute(SimpleStatement("TRUNCATE group_chat_users;"))
    Cassandra.session.execute(SimpleStatement("TRUNCATE private_chats;"))
    Cassandra.session.execute(SimpleStatement("TRUNCATE chats;"))
    john = await user("@john", "John")
    jack = await user("@jack", "Jack")
    mike = await user("@mike", "Mike")
    return {
        "john": {
            "id": john.user_id,
            "chats": [
                await ChatService.create_private_chat(
                    sender_id=john.user_id,
                    receiver_id=jack.user_id,
                    message="hello",
                    sender_name=john.name,
                    receiver_name=jack.name),
                await ChatService.create_group_chat(
                    user_id=john.user_id,
                    chatname="@club",
                    description="",
                    name="")
            ]
        },
        "jack": {
            "id": jack.user_id,
            "chats": [
                await ChatService.create_private_chat(
                    sender_id=jack.user_id,
                    receiver_id=mike.user_id,
                    message="hello",
                    sender_name=jack.name,
                    receiver_name=mike.name)
            ]
        }
    }


@pytest.fixture
async def messages(chats):
    Cassandra.session.execute(SimpleStatement("TRUNCATE unread_messages;"))
    Cassandra.session.execute(SimpleStatement("TRUNCATE messages;"))
    # receiver мы получаем из всех чатов
    receiver = chats["jonh"]["chats"][0][""]
    # sender мы имеем в куках наш айдишник это два
    sender = chats[0]["john"]
    # у груп нет receiver это три
    await MessageService.save(
        chat_id=chats["john"][0].chat_id,
        receiver=chats["john"][0].user_id,
        sender=chats["john"][0].receiver_id,
        text="1"
    )
