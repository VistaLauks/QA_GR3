import pytest
import requests
import allure


# ============================================================
# 1. GET-ЗАПРОСЫ
# ============================================================

@allure.feature("Управление бронированиями")
@allure.story("Получение информации о бронированиях")
class TestGetBookings:

    @allure.title("Получение списка всех бронирований")
    def test_get_all_bookings(self, base_url):
        with allure.step("Отправка GET-запроса на получение всех бронирований"):
            response = requests.get(f"{base_url}/booking")

        with allure.step("Проверка статус-кода и структуры ответа"):
            assert response.status_code == 200, f"GET /booking failed with {response.status_code}"
            bookings = response.json()
            assert isinstance(bookings, list), "Ответ не является списком"
            assert len(bookings) > 0, "Список бронирований пуст"

    @allure.title("Получение конкретного бронирования по ID")
    def test_get_booking_by_id(self, base_url, create_booking_id):
        booking_id = create_booking_id

        with allure.step(f"Отправка GET-запроса для ID: {booking_id}"):
            response = requests.get(f"{base_url}/booking/{booking_id}")

        with allure.step("Проверка корректности данных бронирования"):
            assert response.status_code == 200, f"GET /booking/{booking_id} failed"
            booking = response.json()
            assert booking.get("firstname") == "Ivan", "Имя не совпадает"
            assert booking.get("lastname") == "Petrov", "Фамилия не совпадает"
            assert booking.get("totalprice") == 150, "Цена не совпадает"

    @allure.title("Параметризованный тест для получения бронирований")
    @pytest.mark.parametrize("booking_id", [1, 2, 3])
    def test_get_multiple_bookings(self, base_url, booking_id):
        with allure.step(f"Запрос бронирования с ID {booking_id}"):
            response = requests.get(f"{base_url}/booking/{booking_id}")
        assert response.status_code == 200, f"Booking {booking_id} не найден"
        assert "firstname" in response.json(), "Нет поля firstname"

    @allure.title("Негативный тест: получение несуществующего бронирования")
    def test_get_nonexistent_booking(self, base_url):
        with allure.step("Запрос ID 999999"):
            response = requests.get(f"{base_url}/booking/999999")
        assert response.status_code == 404, f"Ожидался 404, получен {response.status_code}"


# ============================================================
# 2. POST-ЗАПРОСЫ (СОЗДАНИЕ)
# ============================================================

@allure.feature("Управление бронированиями")
@allure.story("Создание бронирований")
class TestCreateBookings:

    @allure.title("Создание бронирования без авторизации")
    def test_create_booking_without_auth(self, base_url):
        payload = {
            "firstname": "John",
            "lastname": "Doe",
            "totalprice": 200,
            "depositpaid": False,
            "bookingdates": {"checkin": "2025-02-01", "checkout": "2025-02-10"},
            "additionalneeds": "Parking"
        }
        with allure.step("Отправка POST-запроса с данными"):
            response = requests.post(f"{base_url}/booking", json=payload)

        with allure.step("Проверка успешного создания"):
            assert response.status_code == 200, "Не удалось создать бронирование"
            data = response.json()
            assert "bookingid" in data, "Нет ID созданного бронирования"
            assert data["booking"]["firstname"] == "John", "Имя не совпадает"


# ============================================================
# 3. PUT / PATCH / DELETE И НЕГАТИВНЫЕ ТЕСТЫ
# ============================================================

@allure.feature("Управление бронированиями")
@allure.story("Модификация и удаление бронирований")
class TestModifyBookings:

    @allure.title("Обновление существующего бронирования через PUT")
    def test_update_booking(self, auth_headers, create_booking_id, base_url):
        booking_id = create_booking_id
        update_payload = {
            "firstname": "Ivan", "lastname": "Sidorov", "totalprice": 250,
            "depositpaid": True,
            "bookingdates": {"checkin": "2025-03-01", "checkout": "2025-03-10"},
            "additionalneeds": "Breakfast and Wi-Fi"
        }
        with allure.step("Отправка PUT-запроса с авторизацией"):
            response = requests.put(f"{base_url}/booking/{booking_id}", json=update_payload, headers=auth_headers)
        assert response.status_code == 200
        assert response.json().get("lastname") == "Sidorov"

    @allure.title("Частичное обновление через PATCH")
    def test_patch_booking(self, auth_headers, create_booking_id, base_url):
        booking_id = create_booking_id
        patch_payload = {"totalprice": 300}
        with allure.step("Отправка PATCH-запроса"):
            response = requests.patch(f"{base_url}/booking/{booking_id}", json=patch_payload, headers=auth_headers)
        assert response.status_code == 200
        assert response.json().get("totalprice") == 300

    @allure.title("Создание и последующее удаление бронирования")
    def test_delete_booking(self, auth_headers, base_url):
        payload = {
            "firstname": "Delete", "lastname": "Me", "totalprice": 50, "depositpaid": False,
            "bookingdates": {"checkin": "2025-01-01", "checkout": "2025-01-02"}
        }
        with allure.step("Создание бронирования"):
            create_resp = requests.post(f"{base_url}/booking", json=payload)
            booking_id = create_resp.json().get("bookingid")

        with allure.step("Удаление бронирования"):
            delete_resp = requests.delete(f"{base_url}/booking/{booking_id}", headers=auth_headers)
        assert delete_resp.status_code in [201, 204]


@allure.feature("Безопасность")
@allure.story("Защита эндпоинтов авторизацией")
class TestSecurityBookings:

    @allure.title("Негативный тест: попытка PUT-обновления без токена")
    def test_update_without_auth(self, create_booking_id, base_url):
        with allure.step("Отправка PUT без заголовков авторизации"):
            response = requests.put(f"{base_url}/booking/{create_booking_id}", json={"firstname": "Hacker"})
        assert response.status_code == 403

    @allure.title("Негативный тест: попытка удаления без токена")
    def test_delete_without_auth(self, create_booking_id, base_url):
        with allure.step("Отправка DELETE без заголовков авторизации"):
            response = requests.delete(f"{base_url}/booking/{create_booking_id}")
        assert response.status_code == 403


if __name__ == "__main__":
    # 2. Обновляем параметры запуска по умолчанию, чтобы собирать allure-результаты
    pytest.main(["-v", "--tb=short", f"--alluredir=allure-results", __file__])
