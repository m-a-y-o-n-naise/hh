import os

class Environment:
    SHOT = 'shot'
    PROD = 'prod' #  класс для управления окружениями Стенд/тестовая сред & Продакшен/боевая среда

    URLS = {
        SHOT: 'https://www.example.ru/',
        PROD: 'https://www.saucedemo.com/'
    } #  URL каждого стенда

    def __init__(self):
        try:
            self.env = os.getenv('ENV') #  Читает переменную окружения ENV из системы
        except KeyError:
            self.env = self.PROD #  Если переменной нет → использует prod по умолчанию

    def get_base_url(self):
        if self.env in self.URLS:
            return self.URLS[self.env] #  Метод get_base_url() возвращает нужный URL
        else:
            raise Exception(f"Unknown value of ENV variable {self.env}") #  ошибка

host = Environment()