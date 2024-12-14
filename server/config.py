from configparser import ConfigParser

# глобальные переменные


DEBUG = True

conf = ConfigParser()

if DEBUG: conf.read('config.cfg')
else: conf.read('conf.cfg')

DB = conf["DATABASE"]

CACHE = {
    "host": conf["CACHE"]["HOST"],
    "password": conf["CACHE"]["PASSWORD"],
    "port": int(conf["CACHE"]["PORT"])
}
