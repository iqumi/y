# y messenger

Оналйн мессенджер, доступный через браузер.

Онлайн платформа для обмена сообщениями в реальном времени, которая позволяет пользователям общаться друг с другом, а так же в беседах через текстовые сообщения и медиафайлы.

За подробностями работы веб приложения: [документация](https://github.com/iqumi/y/blob/main/docs/README.md)

## Как запустить

Демо: comming...

Собрать все у себя, локально:

```bash
git clone https://github.com/iqumi/y && cd y
docker compose up -d
```

Запустить только бэк, при наличии `server/conf.cfg`:

```bash
git clone https://github.com/iqumi/y && cd y
python -m venv env
. env/bin/activate
python -m pip install -r requirements.txt
cd server
fastapi dev main.py
```


#### Структура

```
www/                      # статические файлы веб страницы
server/                   # python App Server
    database/             # настройки подключения к бд
        repositories/     # взаимодействие с бд
        models.py         # слой данных
    services/             # слой бизнес логики
    main.py               # точка входа
```
