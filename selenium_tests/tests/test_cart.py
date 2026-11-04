import pytest
import allure
from allure_commons.types import Severity
import time
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import sys
import os

# Добавляем родительскую папку (selenium_tests) в путь поиска Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from locators.locators_demo import (
    LOGIN_INPUT,
    PASSWORD_INPUT,
    SUBMIT_BUTTON,
    SUBMIT_BUTTON_PRODUCT,
    USER_PROFILE,
    SUBMIT_BUTTON_PRODUCT2,
    REMOVE_BUTTON1,
    REMOVE_BUTTON2,
    CLEAR_SHOP,
)


@allure.step("Логинимся и добавляем товары в корзину: логин = '{login}'")
def fill_login_form(driver, wait, login, password):
    """Заполняем форму входа с использованием локаторов"""
    with allure.step("Заполняем форму входа"):
        login_field = wait.until(EC.element_to_be_clickable(LOGIN_INPUT))
        login_field.clear()
        login_field.send_keys(login)

        password_field = wait.until(EC.element_to_be_clickable(PASSWORD_INPUT))
        password_field.clear()
        password_field.send_keys(password)

        wait.until(EC.element_to_be_clickable(SUBMIT_BUTTON)).click()

    with allure.step("Добавляем товары в корзину"):
        wait.until(EC.element_to_be_clickable(SUBMIT_BUTTON_PRODUCT)).click()
        wait.until(EC.element_to_be_clickable(SUBMIT_BUTTON_PRODUCT2)).click()

    with allure.step("Переходим в корзину"):
        wait.until(EC.element_to_be_clickable(USER_PROFILE)).click()

    with allure.step("Удаляем товары из корзины"):
        wait.until(EC.element_to_be_clickable(REMOVE_BUTTON1)).click()
        wait.until(EC.element_to_be_clickable(REMOVE_BUTTON2)).click()

        time.sleep(2)

@pytest.mark.xfail(reason="Баг: после удаления товаров пользователь остаётся в корзине, а не возвращается на страницу товаров")
@allure.suite("Корзина")                                  # название тест-сьюта
@allure.title("Очистка корзины после удаления товаров")   # название теста
@allure.label("feature", "Корзина")
@allure.label("owner", "Roman Zelenokhat")
@allure.severity(Severity.CRITICAL)
# --- Тесты ---
@pytest.mark.parametrize(
    "login, password",
    [
        ("standard_user", "secret_sauce"),
    ],
    ids=[
        "valid_credentials"
    ]
)
# Прогоняем тесты с полученными параметрами на веб-интерфейсе
def test_login(driver, wait, login, password):
    with allure.step("Открываем страницу авторизации"):
        driver.get("https://www.saucedemo.com/")  # URL адреса сайта

    with allure.step("Выполняем сценарий: логин, добавление и удаление товаров"):
        fill_login_form(driver, wait, login, password)

    # Тест на очищенную корзину
    with allure.step("Проверяем, что корзина пуста"):
        wait.until(EC.visibility_of_element_located(CLEAR_SHOP))

    # Тест на нахождение пользователя на странице выбора товаров (должен упасть с ошибкой)
    with allure.step("Проверяем, что пользователь вернулся на страницу выбора товаров"):
        try:
            wait.until(EC.visibility_of_element_located(SUBMIT_BUTTON_PRODUCT))
        except TimeoutException:
            assert False, "Пользователь не на странице выбора товаров"



