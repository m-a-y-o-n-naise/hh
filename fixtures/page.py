import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright
import os



def pytest_addoption(parser):
    """Пользовательские опции командной строки"""
    parser.addoption('--bn', action='store', default="chrome", help="Choose browser: chrome, remote_chrome or firefox") #  выбор браузера (chrome/firefox/remote_chrome)
    parser.addoption('--h', action='store', default=False, help='Choose headless: True or False') #  headless-режим (без GUI).
    parser.addoption('--s', action='store', default={'width': 1920, 'height': 1080}, help='Size window: width,height') #  размер окна.
    parser.addoption('--slow', action='store', default=200, help='Choose slow_mo for robot action') #  замедление действий (в миллисекундах).
    parser.addoption('--t', action='store', default=60000, help='Choose timeout') #  таймаут ожидания элементов.
    parser.addoption('--l', action='store', default='ru-RU', help='Choose locale') #  локаль (язык браузера).
    # parser.addini('qs_to_api_token', default=os.getenv("QASE_TOKEN"), help='Qase app token')



@pytest.fixture(scope='class')
def browser(request) -> Page:
    playwright = sync_playwright().start() #  Запуск Playwright
    if request.config.getoption("bn") == 'remote_chrome': #  Проверка параметра --bn из командной строки
        browser = get_remote_chrome(playwright, request) #  Вызов функции для создания удалённого Chrome
        context = get_context(browser, request, 'remote')
        page_data = context.new_page() #  Создание новой вкладки
    elif request.config.getoption("bn") == 'firefox':
        browser = get_firefox_browser(playwright, request)
        context = get_context(browser, request, 'local')
        page_data = context.new_page()
    elif request.config.getoption("bn") == 'chrome':
        browser = get_chrome_browser(playwright, request)
        context = get_context(browser, request, 'local')
        page_data = context.new_page()
    else:
        browser = get_chrome_browser(playwright, request)
        context = get_context(browser, request, 'local')
        page_data = context.new_page()
    yield page_data #  Возврат страницы тестам. После тестов выполняется код ниже
    for context in browser.contexts:
        context.close() #  Очистка: закрытие контекстов
    browser.close() #  Очистка: закрытие браузера
    playwright.stop() #  Очистка: остановка Playwright


def get_firefox_browser(playwright, request) -> Browser:
    return playwright.firefox.launch(
        headless=request.config.getoption("h"),
        slow_mo=request.config.getoption("slow"),
    ) #  Функция запуска Firefox с параметрами headless и slow_mo


def get_chrome_browser(playwright, request) -> Browser:
    return playwright.chromium.launch(
        headless=request.config.getoption("h"),
        slow_mo=request.config.getoption("slow"),
        args=['--start-maximized']
    )

def get_remote_chrome(playwright, request) -> Browser:
    return playwright.chromium.launch(
        headless=True,
        slow_mo=request.config.getoption("slow")
    )


def get_context(browser, request, start) -> BrowserContext:
    if start == 'local':
        context = browser.new_context(
            no_viewport=True,
            locale=request.config.getoption('l')
        ) # no_viewport=True — окно на весь экран, locale — язык интерфейса
        context.set_default_timeout(
            timeout=request.config.getoption('t')
        ) #  Установка таймаута по умолчанию для ожиданий
        # context.add_cookies([{'url': 'https://example.ru', 'name': 'ab_test', 'value': 'd'}]) добавляем куки, если нужны
        return context

    elif start == 'remote':
        context = browser.new_context(
            viewport=request.config.getoption('s'),
            locale=request.config.getoption('l')
        )
        context.set_default_timeout(
            timeout=request.config.getoption('t')
        )
        # context.add_cookies([{'url': 'https://example.ru', 'name': 'ab_test', 'value': 'd'}]) добавляем куки, если нужны
        return context



@pytest.fixture(scope="function")
def return_back(browser):
    browser.go_back() #  Фикстура возврата на предыдущую страницу