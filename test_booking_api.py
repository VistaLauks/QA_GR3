import pytest
import requests


# ============================================================
# 1. GET-ЗАПРОСЫ
# ============================================================

def test_get_all_bookings(base_url):
    """Получение списка всех бронирований"""
    response = requests.get(f"{base_url}/booking")
    assert response.status_code == 200, f"GET /booking failed with {response.status_code}"
    bookings = response.json()
    assert isinstance(bookings, list), "Ответ не является списком"
    assert len(bookings) > 0, "Список бронирований пуст"


def test_get_booking_by_id(base_url, create_booking_id):
    """Получение конкретного бронирования по ID"""
    booking_id = create_booking_id
    response = requests.get(f"{base_url}/booking/{booking_id}")
    assert response.status_code == 200, f"GET /booking/{booking_id} failed"
    booking = response.json()
    assert booking.get("firstname") == "Ivan", "Имя не совпадает"
    assert booking.get("lastname") == "Petrov", "Фамилия не совпадает"
    assert booking.get("totalprice") == 150, "Цена не совпадает"


@pytest.mark.parametrize("booking_id", [1, 2, 3])
def test_get_multiple_bookings(base_url, booking_id):
    """Параметризованный тест для нескольких ID"""
    response = requests.get(f"{base_url}/booking/{booking_id}")
    assert response.status_code == 200, f"Booking {booking_id} не найден"
    assert "firstname" in response.json(), "Нет поля firstname"


def test_get_nonexistent_booking(base_url):
    """Негативный тест: несуществующее бронирование → 404"""
    response = requests.get(f"{base_url}/booking/999999")
    assert response.status_code == 404, f"Ожидался 404, получен {response.status_code}"


# ============================================================
# 2. POST-ЗАПРОСЫ (СОЗДАНИЕ)
# ============================================================

def test_create_booking_without_auth(base_url):
    """Создание бронирования без авторизации (должно работать)"""
    payload = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 200,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2025-02-01",
            "checkout": "2025-02-10"
        },
        "additionalneeds": "Parking"
    }
    response = requests.post(f"{base_url}/booking", json=payload)
    assert response.status_code == 200, "Не удалось создать бронирование"
    data = response.json()
    assert "bookingid" in data, "Нет ID созданного бронирования"
    assert data["booking"]["firstname"] == "John", "Имя не совпадает"


# ============================================================
# 3. PUT-ЗАПРОСЫ (ОБНОВЛЕНИЕ)
# ============================================================

def test_update_booking(auth_headers, create_booking_id, base_url):
    """Обновление существующего бронирования через PUT"""
    booking_id = create_booking_id
    update_payload = {
        "firstname": "Ivan",
        "lastname": "Sidorov",
        "totalprice": 250,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-03-01",
            "checkout": "2025-03-10"
        },
        "additionalneeds": "Breakfast and Wi-Fi"
    }
    response = requests.put(
        f"{base_url}/booking/{booking_id}",
        json=update_payload,
        headers=auth_headers
    )
    assert response.status_code == 200, f"PUT failed with {response.status_code}"
    updated = response.json()
    assert updated.get("lastname") == "Sidorov", "Фамилия не обновилась"
    assert updated.get("totalprice") == 250, "Цена не обновилась"


# ============================================================
# 4. PATCH-ЗАПРОСЫ (ЧАСТИЧНОЕ ОБНОВЛЕНИЕ)
# ============================================================

def test_patch_booking(auth_headers, create_booking_id, base_url):
    """Частичное обновление через PATCH (меняем только цену)"""
    booking_id = create_booking_id
    patch_payload = {"totalprice": 300}
    response = requests.patch(
        f"{base_url}/booking/{booking_id}",
        json=patch_payload,
        headers=auth_headers
    )
    assert response.status_code == 200, f"PATCH failed with {response.status_code}"
    patched = response.json()
    assert patched.get("totalprice") == 300, "Цена не обновилась"
    # Проверяем, что остальные поля не изменились
    assert patched.get("firstname") == "Ivan", "Имя изменилось (а должно остаться)"


# ============================================================
# 5. DELETE-ЗАПРОСЫ (УДАЛЕНИЕ)
# ============================================================

def test_delete_booking(auth_headers, base_url):
    """Создаём бронирование и сразу удаляем его"""
    payload = {
        "firstname": "Delete",
        "lastname": "Me",
        "totalprice": 50,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2025-01-01",
            "checkout": "2025-01-02"
        }
    }
    create_resp = requests.post(f"{base_url}/booking", json=payload)
    assert create_resp.status_code == 200, "Не удалось создать бронирование для удаления"
    booking_id = create_resp.json().get("bookingid")

    delete_resp = requests.delete(
        f"{base_url}/booking/{booking_id}",
        headers=auth_headers
    )
    assert delete_resp.status_code in [201, 204], f"DELETE вернул {delete_resp.status_code}"


# ============================================================
# 6. НЕГАТИВНЫЕ ТЕСТЫ (БЕЗ АВТОРИЗАЦИИ)
# ============================================================

def test_update_without_auth(create_booking_id, base_url):
    """Обновление без авторизации → 403"""
    booking_id = create_booking_id
    response = requests.put(
        f"{base_url}/booking/{booking_id}",
        json={"firstname": "Hacker"}
    )
    assert response.status_code == 403, f"Ожидался 403, получен {response.status_code}"


def test_delete_without_auth(create_booking_id, base_url):
    """Удаление без авторизации → 403"""
    booking_id = create_booking_id
    response = requests.delete(f"{base_url}/booking/{booking_id}")
    assert response.status_code == 403, f"Ожидался 403, получен {response.status_code}"


# ============================================================
# 7. ЗАПУСК
# ============================================================

if __name__ == "__main__":
    pytest.main(["-v", "--tb=short", __file__])