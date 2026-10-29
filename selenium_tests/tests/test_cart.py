import pytest
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

# Сценарии тестов
def fill_login_form(driver, wait, login, password):
    """Заполняем форму входа с использованием локаторов"""
    login_field = wait.until(EC.visibility_of_element_located(LOGIN_INPUT))
    login_field.clear()
    login_field.send_keys(login)

    password_field = driver.find_element(*PASSWORD_INPUT)
    password_field.clear()
    password_field.send_keys(password)

    submit_btn = driver.find_element(*SUBMIT_BUTTON)
    submit_btn.click()

    submit_btn_product = driver.find_element(*SUBMIT_BUTTON_PRODUCT)
    submit_btn_product.click()

    submit_btn_product2 = driver.find_element(*SUBMIT_BUTTON_PRODUCT2)
    submit_btn_product2.click()

    submit_btn_profile = driver.find_element(*USER_PROFILE)
    submit_btn_profile.click()

    remove_btn1 = driver.find_element(*REMOVE_BUTTON1)
    remove_btn1.click()

    remove_btn2 = driver.find_element(*REMOVE_BUTTON2)
    remove_btn2.click()

    time.sleep(2)


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
# Прогоняем тесты с полученными параметрами на Веб-интерфейсе, разделяяя их на положительный и отрицательные
def test_login(driver, wait, login, password):
    driver.get("https://www.saucedemo.com/")  # URL адреса сайта
    fill_login_form(driver, wait, login, password)

    #Тест на очищенную корзину
    wait.until(EC.visibility_of_element_located(CLEAR_SHOP))
    #Тест на нахождение пользователя на странице выбора товаров (Должен упасть с ошибкой) selenium_tests\tests\cart.py:97:
    try:
        submit_button = wait.until(EC.visibility_of_element_located(SUBMIT_BUTTON_PRODUCT))
    except TimeoutException:
        assert False, "Пользователь не на странице выбора товаров"



