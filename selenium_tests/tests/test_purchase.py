import pytest
import allure
from allure_commons.types import Severity
import time
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
    CHECK_OUT,
    FIRST_NAME,
    LAST_NAME,
    POSTAL_CODE,
    CONTINUE_BUTTON,
    FINISH_BUTTON,
    COMPLETE_OUTPUT,
)


@allure.step("Сценарий покупки: логин = '{login}', покупатель = {firstname} {lastname}")
def fill_login_form(driver, wait, login, password, firstname, lastname, postalcode):
    with allure.step("Заполняем форму входа"):
        login_field = wait.until(EC.element_to_be_clickable(LOGIN_INPUT))
        login_field.clear()
        login_field.send_keys(login)

        password_field = wait.until(EC.element_to_be_clickable(PASSWORD_INPUT))
        password_field.clear()
        password_field.send_keys(password)

        wait.until(EC.element_to_be_clickable(SUBMIT_BUTTON)).click()

    with allure.step("Добавляем товар в корзину и переходим в корзину"):
        wait.until(EC.element_to_be_clickable(SUBMIT_BUTTON_PRODUCT)).click()
        wait.until(EC.element_to_be_clickable(USER_PROFILE)).click()

    with allure.step("Нажимаем Checkout и заполняем данные покупателя"):
        wait.until(EC.element_to_be_clickable(CHECK_OUT)).click()

        firstname_field = wait.until(EC.element_to_be_clickable(FIRST_NAME))
        firstname_field.clear()
        firstname_field.send_keys(firstname)

        lastname_field = wait.until(EC.element_to_be_clickable(LAST_NAME))
        lastname_field.clear()
        lastname_field.send_keys(lastname)

        postalcode_field = wait.until(EC.element_to_be_clickable(POSTAL_CODE))
        postalcode_field.clear()
        postalcode_field.send_keys(postalcode)

        wait.until(EC.element_to_be_clickable(CONTINUE_BUTTON)).click()

    with allure.step("Завершаем покупку (Finish)"):
        wait.until(EC.element_to_be_clickable(FINISH_BUTTON)).click()
        time.sleep(2)


@allure.suite("Оформление заказа")                          # название тест-сьюта
@allure.title("Успешная покупка товара")                    # название теста
@allure.label("feature", "Checkout")
@allure.label("owner", "Roman Zelenokhat")
@allure.severity(Severity.BLOCKER)
# --- Тесты ---
@pytest.mark.parametrize(
    "login,password, firstname, lastname, postalcode",
    [
        ("standard_user", "secret_sauce", "roman", "zelenokhat", "123"),  # Успешная покупка товара
    ],
    ids=[
        "valid_credentials"
    ]
)
# Прогоняем тесты с полученными параметрами на веб-интерфейсе
def test_login(driver, wait, login, password, firstname, lastname, postalcode):
    with allure.step("Открываем страницу авторизации"):
        driver.get("https://www.saucedemo.com/")  # URL адреса сайта

    with allure.step("Выполняем сценарий: логин, покупка товара"):
        fill_login_form(driver, wait, login, password, firstname, lastname, postalcode)

    with allure.step("Проверяем, что покупка завершена успешно"):
        wait.until(EC.visibility_of_element_located(COMPLETE_OUTPUT))
        assert True, "Успешная покупка"
