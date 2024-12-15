import pytest

from services import UserService, ChatService, MessageService


@pytest.fixture
async def create_user():
    return UserService.create_user

@pytest.fixture
async def send_message():
    return MessageService.send_message


@pytest.fixture
async def users(create_user):
    return {
        "john": await create_user("@john", "John"),
        "bill": await create_user("@bill", "Bill"),
        "mike": await create_user("@mike", "Mike"),
    }


@pytest.fixture
async def john_chats(users):
    return [
        await ChatService.create_private_chat(
            users["john"].user_id,
            users["bill"].user_id),
        await ChatService.create_group_chat(
            users["john"].user_id,
            "@cool_chatname",
            "cool name"),
    ]


@pytest.fixture
async def bill_chat(users):
    return await ChatService.create_private_chat(
        users["bill"].user_id,
        users["mike"].user_id)


@pytest.fixture
async def messages(send_message, john_chats, bill_chat, users):
    return [
        await send_message(john_chats[1].chat_id, users["john"].user_id, "yo"),
        await send_message(john_chats[0].chat_id, users["john"].user_id, "hi"),
        await send_message(john_chats[0].chat_id, users["john"].user_id, "how are ya"),
        await send_message(john_chats[0].chat_id, users["bill"].user_id, "good"),
        await send_message(bill_chat.chat_id, users["bill"].user_id, "yo"),
    ]
