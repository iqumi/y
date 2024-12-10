from configparser import ConfigParser

# глобальные переменные


DEBUG = True

prodconf = ConfigParser()
prodconf.read('conf.cfg')

testconf = ConfigParser()
testconf.read('config.cfg')

DATABASES = {
    "prod": {
        "USERNAME": prodconf['DEFAULT']['USERNAME'],
        "PASSWORD": prodconf['DEFAULT']['PASSWORD'],
        "IP": prodconf['DEFAULT']['IP'],
        "PORT": prodconf['DEFAULT']['PORT']
    },
    "test": {
        "USERNAME": testconf['TEST']['USERNAME'],
        "PASSWORD": testconf['TEST']['PASSWORD'],
        "IP": testconf['TEST']['IP'],
        "PORT": testconf['TEST']['PORT']
    }
}

if DEBUG: DB = DATABASES["test"]
else: DB = DATABASES["prod"]
