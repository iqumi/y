from configparser import ConfigParser
from enum import Enum

# глобальные переменные

config = ConfigParser()
config.read('conf.cfg')


DEBUG = True

DATABASES = {
    "docker": {
        "USERNAME": "cassandra",
        "PASSWORD": "cassandra",
        "IP": "database",
        "PORT": 9042
    },
    "prod": {
        "USERNAME": config['DEFAULT']['USERNAME'],
        "PASSWORD": config['DEFAULT']['PASSWORD'],
        "IP": config['DEFAULT']['IP'],
        "PORT": config['DEFAULT']['PORT']
    }
}

if DEBUG: DB = DATABASES["docker"]
else: DB = DATABASES["prod"]


"""Типы Enums"""

class UserStatus(Enum):
    USER = "user"
    ADMIN = "admin"

class ChatTypes(Enum):
    PRIVATE = "private"
    GROUP = "group"
