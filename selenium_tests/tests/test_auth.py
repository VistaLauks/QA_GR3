import pytest
import allure
from allure_commons.types import Severity
from selenium.webdriver.support import expected_conditions as EC
import sys
import os

# Добавляем родительскую папку (selenium_tests) в путь поиска Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импорт локаторов из locators_demo
from locators.locators_demo import (
    LOGIN_INPUT,
    PASSWORD_INPUT,
    SUBMIT_BUTTON,
    ERROR_MESSAGE,
    USER_PROFILE,
)


@allure.step("Заполняем форму входа: логин = '{login}'")
def fill_login_form(driver, wait, login, password):
    """Заполняем форму входа с использованием локаторов"""
    with allure.step("Вводим логин"):
        login_field = wait.until(EC.visibility_of_element_located(LOGIN_INPUT))
        login_field.clear()
        login_field.send_keys(login)

    with allure.step("Вводим пароль"):
        password_field = driver.find_element(*PASSWORD_INPUT)
        password_field.clear()
        password_field.send_keys(password)

    with allure.step("Нажимаем кнопку входа"):
        submit_btn = driver.find_element(*SUBMIT_BUTTON)
        submit_btn.click()


@allure.suite("Авторизация")                     # название тест-сьюта
@allure.title("Авторизация на сайте")            # название теста (для параметризованных — общее)
@allure.label("feature", "Логин")
@allure.label("owner", "Roman Zelenokhat")
@allure.severity(Severity.CRITICAL)
# Прогоняем тесты с полученными параметрами на веб-интерфейсе, разделяя их на положительный и отрицательные
@pytest.mark.parametrize(
    "login,password,expected_success,err_message",
    [
        ("standard_user", "secret_sauce", True, None),   # 1. Положительный вход
        ("", "secret_sauce", False, "epic sadface: username is required"),          # 2. Ошибка: пустой логин
        ("standard_user", "", False, "epic sadface: password is required"),         # 3. Ошибка: пустой пароль
        ("wrong_user", "wrong_password", False, "epic sadface: username and password do not match any user in this service"),  # 4. Ошибка: неверные данные
    ],
    ids=[
        "valid_credentials",
        "empty_login",
        "empty_password",
        "invalid_credentials"
    ]
)
def test_login(driver, wait, login, password, expected_success, err_message):
    with allure.step("Открываем страницу авторизации"):
        driver.get("https://www.saucedemo.com/")  # URL адреса сайта

    with allure.step("Заполняем и отправляем форму входа"):
        fill_login_form(driver, wait, login, password)

    if expected_success:
        # Проверяем, что вход успешен (появился элемент профиля/личный кабинет)
        with allure.step("Проверяем, что выполнен успешный вход"):
            wait.until(EC.visibility_of_element_located(USER_PROFILE))
            assert True, "Успешный вход подтверждён"
    else:
        # Проверяем, что появилась ошибка
        with allure.step("Проверяем, что появилось сообщение об ошибке"):
            error_element = wait.until(EC.visibility_of_element_located(ERROR_MESSAGE))
            assert error_element.is_displayed(), "Сообщение об ошибке должно быть видно"
            # Дополнительно можно проверить текст ошибки, если нужно:
            assert err_message in error_element.text.lower()
