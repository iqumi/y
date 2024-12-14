from pydantic import UUID4

from schemas import api
from database import Valkey
from database.models import Chat, GroupChat, Tag
from database.repositories import TagRepository, \
    ChatRepository, GroupChatRepository


class ChatService:
    """
    Определяет бизнес логику,
    абстрагирует работу с чатами
    """
    tags = TagRepository()
    groups = GroupChatRepository()
    chats = ChatRepository()

    @classmethod
    async def get_user_chats(
        cls,
        user_id: UUID4
    ) -> list[api.Chat]:
        """
        Получить все чаты и беседы пользователя по user_id
        >>> await ChatService.get_user_chats(user_id)
        """
        chats = [api.Chat(**i.__dict__) async for i in cls.chats.get(user_id)]

        n = Valkey.session.mget([f"user:{i.user_chat_id}:name" for i in chats])
        m = Valkey.session.mget([f"chat:{i.chat_id}:message" for i in chats])

        for i, chat in enumerate(chats):
            chats[i].last_message = m[i]
            chats[i].name = n[i]

        return chats

    @classmethod
    async def create_private_chat(
        cls,
        sender_id: UUID4,
        receiver_id: UUID4,
    ) -> api.Chat:
        """Создать новый приватный чат"""
        chat = Chat(sender_id, receiver_id)
        opposite = Chat(receiver_id, sender_id, chat.chat_id)
        c = await cls.chats.save(chat)
        await cls.chats.save(opposite)
        name = Valkey.session.get(f"user:{receiver_id}:name")
        return api.Chat(**c.__dict__, name=name)

    @classmethod
    async def create_group_chat(
        cls,
        user_id: UUID4,
        chatname: str,
        name: str,
        description: str = "",
    ) -> api.Chat:
        """Создать новую беседу"""
        tag = await cls.tags.save(Tag(chatname))
        await cls.groups.save(GroupChat(
            chat_id=tag.id,
            user_id=user_id,
            description=description,
            name=name,
            nickname="Owner",
            is_admin=True))
        chat = await cls.chats.save(Chat(
            user_id=user_id,
            user_chat_id=tag.id,
            chat_id=tag.id))

        msg = "Беседа только что создана"
        Valkey.session.set(f"user:{tag.id}:name", name)
        Valkey.session.set(f"chat:{tag.id}:message", msg)

        return api.Chat(
            user_id=chat.user_id,
            user_chat_id=chat.user_chat_id,
            chat_id=chat.chat_id,
            name=name,
            last_message=msg
        )

    def add_user(self):
        pass
