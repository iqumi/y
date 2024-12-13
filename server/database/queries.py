
# Запросы к бд


class TagQueries:
    FIND = "SELECT * FROM tags WHERE tag=?"
    SAVE = """
        INSERT INTO tags (
            tag, id
        ) VALUES (
            %(tag)s,
            %(id)s
        ) IF NOT EXISTS"""
    CREATE = """
        CREATE TABLE IF NOT EXISTS tags (
            tag text PRIMARY KEY,
            id UUID)"""


class UserQueries:
    FIND = "SELECT * FROM users WHERE user_id=?"
    SAVE = """
        INSERT INTO users (
            user_id, name, email, bio
        ) VALUES (
            %(user_id)s,
            %(name)s
            %(email)s,
            %(bio)s,
        ) IF NOT EXISTS"""
    CREATE = """
        CREATE TABLE IF NOT EXISTS users (
            user_id UUID PRIMARY KEY,
            name text,
            email text,
            bio text);"""


class ChatQueries:
    GET = "SELECT * FROM chats WHERE user_id=?"
    SAVE = """
        INSERT INTO chats (
            user_id, user_chat_id, chat_id
        ) VALUES (
            %(user_id)s,
            %(user_chat_id)s,
            %(chat_id)s
        ) IF NOT EXISTS
        """
    CREATE = """
        CREATE TABLE IF NOT EXISTS chats(
            user_id UUID,
            user_chat_id UUID,
            chat_id UUID,
            PRIMARY KEY (user_id, user_chat_id))
        WITH CLUSTERING ORDER BY (user_chat_id DESC);
        """


class GroupChatQueries:
    GET = "SELECT * FROM group_chats WHERE chat_id=?"
    SAVE = """
        INSERT INTO group_chats (
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
        CREATE TABLE IF NOT EXISTS group_chats (
            chat_id UUID,
            user_id UUID,
            description text STATIC,
            name text STATIC,
            nickname text,
            is_admin boolean,
            PRIMARY KEY (chat_id, user_id));
            """


class MessageQueries:
    GET = "SELECT * FROM messages WHERE chat_id=? AND yaer_month=?"
    FIND = GET + " AND message_id=?"
    DELETE = "DELETE FROM messages WHERE chat_id=? and year_month=? AND message_id=?"
    SAVE = """
        INSERT INTO messages (
            chat_id, year_month, message_id, created_at, read_at, sender, data, text
        ) VALUES (
            %(chat_id)s,
            %(year_month)s,
            %(message_id)s,
            %(created_at)s,
            %(read_at)s,
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
    "tags": TagQueries,
    "users": UserQueries,

    "chats": ChatQueries,
    "group_chats": GroupChatQueries,

    "messages": MessageQueries,
    "unread_messages": UnreadMessageQueries,
}
