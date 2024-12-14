import pytest
from cassandra.query import SimpleStatement

from services import UserService, ChatService, MessageService
from database import Cassandra, Valkey
from database import models as m


@pytest.fixture
async def user():
    Valkey.session.flushdb()
    Cassandra.session.execute(SimpleStatement("TRUNCATE tags;"))
    Cassandra.session.execute(SimpleStatement("TRUNCATE users;"))
    return UserService.create_user


@pytest.fixture
async def chats(user):
    Valkey.session.flushdb()
    Cassandra.session.execute(SimpleStatement("TRUNCATE tags;"))
    Cassandra.session.execute(SimpleStatement("TRUNCATE group_chats;"))
    Cassandra.session.execute(SimpleStatement("TRUNCATE chats;"))

    john = await user("@john", "John")
    jack = await user("@jack", "Jack")
    mike = await user("@mike", "Mike")

    john_group = await ChatService.create_group_chat(
        user_id=john.user_id,
        chatname="@cool_club",
        name="cool name")
    john_private = await ChatService.create_private_chat(
        sender_id=john.user_id,
        receiver_id=jack.user_id)
    jack_private = await ChatService.create_private_chat(
        sender_id=jack.user_id,
        receiver_id=mike.user_id)

    return {
        "john": {
            "user": john,
            "chats": {
                "private": john_private,
                "group": john_group
            }
        },
        "jack": {
            "user": jack,
            "chats": {
                "private": jack_private
            }
        }
    }


@pytest.fixture
async def messages(chats):
    Valkey.session.flushdb()
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
