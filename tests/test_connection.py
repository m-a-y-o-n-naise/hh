import pytest
import requests


def test_saucedemo_available():
    """Проверка доступности тестового сайта"""
    response = requests.get('https://www.saucedemo.com', timeout=10)
    assert response.status_code == 200, f"Сайт недоступен. Статус: {response.status_code}"


def test_site_loads():
    """Проверка заголовка страницы"""
    response = requests.get('https://www.saucedemo.com')
    assert 'Swag Labs' in response.text, "Неверный контент страницы"