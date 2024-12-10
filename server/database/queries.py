
# Запросы к бд


class UsersnameQueries:
    # The price we have to pay for data consistency...
    # two queries: find user_id then get user data from users
    FIND = "SELECT * FROM users_by_name WHERE username=?"
    SAVE = """
        INSERT INTO users_by_name (
            username, user_id
        ) VALUES (
            %(username)s,
            %(user_id)s
        ) IF NOT EXISTS"""
    CREATE = """
        CREATE TABLE IF NOT EXISTS users_by_name (
            username text PRIMARY KEY,
            user_id UUID)"""


class ChatnameQueries:
    FIND = "SELECT * FROM chats_by_name WHERE chatname=?"
    SAVE = """
        INSERT INTO chats_by_name (
            chatname, chat_id
        ) VALUES (
            %(chatname)s,
            %(chat_id)s
        ) IF NOT EXISTS"""
    CREATE = """CREATE TABLE IF NOT EXISTS chats_by_name (
        chatname text PRIMARY KEY,
        chat_id UUID)"""


class UserQueries:
    FIND = "SELECT * FROM users WHERE user_id=?"
    SAVE = """
        INSERT INTO users (
            user_id, bio, name
        ) VALUES (
            %(user_id)s,
            %(bio)s,
            %(name)s
        ) IF NOT EXISTS"""
    CREATE = """
        CREATE TABLE IF NOT EXISTS users (
            user_id UUID PRIMARY KEY,
            name text,
            bio text);"""


"""Разграничение"""


class GroupChatQueries:
    GET = "SELECT * FROM group_chat_users WHERE chat_id=?"
    SAVE = """
        INSERT INTO group_chat_users (
            chat_id, user_id, description, name, nickname, is_admin
        ) VALUES (
            %(chat_id)s,
            %(user_id)s,
            %(description)s,
            %(name)s,
            %(nickname)s,
            %(is_admin)s
        ) IF NOT EXISTS
        """
    CREATE = """
        CREATE TABLE IF NOT EXISTS group_chat_users(
            chat_id UUID,
            user_id UUID,
            description text STATIC,
            name text STATIC,
            nickname text,
            is_admin boolean,
            PRIMARY KEY (chat_id, user_id));
            """


class PrivateChatQueries:
    """Для создания уникальных связок user-user"""
    """TODO: Надо бы пересмотреть и пересчитать эту"""
    SAVE = """
        INSERT INTO private_chats (
            user1_id, user2_id, chat_id
        ) VALUES (
            %(user1_id)s,
            %(user2_id)s,
            %(chat_id)s
        ) IF NOT EXISTS
        """
    CREATE = """
        CREATE TABLE IF NOT EXISTS private_chats(
            user1_id UUID,
            user2_id UUID,
            chat_id UUID,
            PRIMARY KEY ((user1_id, user2_id)));
            """


class ChatQueries:
    GET = "SELECT * FROM chats WHERE user_id=?"
    UPDATE = """
        UPDATE chats
        SET %(field)s = %(field)s
        WHERE user_id in %(users)s
        AND chat_id = %(chat_id)s
        """
    SAVE = """
        INSERT INTO chats (
            user_id, chat_id, last_message, is_private, name
        ) VALUES (
            %(user_id)s,
            %(chat_id)s,
            %(last_message)s,
            %(is_private)s,
            %(name)s
        ) IF NOT EXISTS
        """
    CREATE = """
        CREATE TABLE IF NOT EXISTS chats(
            user_id UUID,
            chat_id UUID,
            last_message text,
            is_private boolean,
            name text,
            PRIMARY KEY (user_id, chat_id))
        WITH CLUSTERING ORDER BY (chat_id DESC);
        """


"""Разграничение"""


class MessageQueries:
    GET = "SELECT * FROM messages WHERE chat_id=? AND yaer_month=?"
    FIND = GET + " AND message_id=?"
    DELETE = "DELETE FROM messages WHERE chat_id=? and year_month=? AND message_id=?"
    SAVE = """
        INSERT INTO messages (
            chat_id, year_month, message_id, created_at, read_at, receiver, sender, data, text
        ) VALUES (
            %(chat_id)s,
            %(year_month)s,
            %(message_id)s,
            %(created_at)s,
            %(read_at)s,
            %(receiver)s,
            %(sender)s,
            %(data)s,
            %(text)s,
        ) IF NOT EXISTS
        """
    CREATE = """
        CREATE TABLE IF NOT EXISTS messages (
            chat_id UUID,
            year_month text,
            message_id UUID,
            created_at timestamp,
            read_at timestamp,
            receiver UUID,
            sender UUID,
            data text,
            text text,
            PRIMARY KEY ((chat_id, year_month), message_id, created_at))
        WITH CLUSTERING ORDER BY (message_id DESC, created_at DESC);
        """


class UnreadMessageQueries:
    GET = "SELECT * FROM unread_messages WHERE user_id=?"
    DELETE = "DELETE FROM unread_messages WHERE user_id=? and chat_id=? AND message_id=?"
    SAVE = """
        INSERT INTO unread_messages (
            user_id, chat_id, message_id, created_at, sender, text
        ) VALUES (
            %(user_id)s,
            %(chat_id)s,
            %(message_id)s,
            %(created_at)s,
            %(sender)s,
            %(text)s,
        ) IF NOT EXISTS
        """
    CREATE = """
        CREATE TABLE IF NOT EXISTS unread_messages (
            user_id UUID,
            chat_id UUID,
            message_id UUID,
            created_at timestamp,
            sender UUID,
            text text,
            PRIMARY KEY ((user_id), chat_id, message_id, created_at))
        WITH CLUSTERING ORDER BY (chat_id DESC, message_id DESC, created_at DESC);
        """


R = {'class':'SimpleStrategy', 'replication_factor' : 1}
KEYSPACE = f"CREATE KEYSPACE IF NOT EXISTS chat WITH replication = {R};"

QUERIES = {
    # для создания уникальных имен
    "users_by_name": UsersnameQueries ,
    "chats_by_name": ChatnameQueries,
    "users": UserQueries,

    "group_chat_users": GroupChatQueries,
    "private_chats": PrivateChatQueries,
    "chats": ChatQueries,

    "unread_messages": UnreadMessageQueries,
    "messages": MessageQueries,
}
