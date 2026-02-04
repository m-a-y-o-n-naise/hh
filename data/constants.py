import os

class Constants:
    try:
        login = os.getenv('AUTH_LOGIN')
        password = os.getenv('AUTH_PASSWORD')
    except KeyError:
        print("LOGIN OR PW WASN'T FOUND") #  Это нужно, чтобы не хранить авторизационные креды в коде.
        # Логин и пароль при запуске локально будет подтягиваться из
        # файла .env, а при удаленном запуске — из папок secrets.