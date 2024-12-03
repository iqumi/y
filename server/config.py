from configparser import ConfigParser

# глобальные переменные

config = ConfigParser()
config.read('conf.cfg')


DEBUG = False

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
