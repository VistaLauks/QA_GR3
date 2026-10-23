import pytest
import requests

@pytest.fixture(scope="session")
def base_url():
    """Базовая URL для API"""
    return "https://restful-booker.herokuapp.com"

@pytest.fixture(scope="session")
def auth_token(base_url):
    """Получение токена авторизации (один раз за сессию)"""
    auth_payload = {
        "username": "admin",
        "password": "password123"
    }
    response = requests.post(f"{base_url}/auth", json=auth_payload)
    assert response.status_code == 200, "Не удалось получить токен"
    token = response.json().get("token")
    assert token is not None, "Токен не найден в ответе"
    return token

@pytest.fixture
def auth_headers(auth_token):
    """Заголовки с токеном для авторизованных запросов"""
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cookie": f"token={auth_token}"
    }

@pytest.fixture
def create_booking_id(base_url):
    """Создаёт бронирование и возвращает его ID (с автоматическим удалением после теста)"""
    payload = {
        "firstname": "Ivan",
        "lastname": "Petrov",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-01-01",
            "checkout": "2025-01-05"
        },
        "additionalneeds": "Breakfast"
    }
    response = requests.post(f"{base_url}/booking", json=payload)
    assert response.status_code == 200, "Не удалось создать бронирование"
    booking_id = response.json().get("bookingid")
    assert booking_id is not None, "ID бронирования не найден"

    yield booking_id

    # Удаляем бронирование ПОСЛЕ теста
    auth_payload = {"username": "admin", "password": "password123"}
    auth_resp = requests.post(f"{base_url}/auth", json=auth_payload)
    token = auth_resp.json().get("token")
    headers = {"Cookie": f"token={token}"}
    delete_response = requests.delete(f"{base_url}/booking/{booking_id}", headers=headers)
    assert delete_response.status_code in [201, 204], "Не удалось удалить бронирование"