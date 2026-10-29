import pytest
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

# Сценарии тестов
def fill_login_form(driver, wait, login, password, firstname,lastname, postalcode):
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

    submit_btn_profile = driver.find_element(*USER_PROFILE)
    submit_btn_profile.click()

    submit_btn_checkout = driver.find_element(*CHECK_OUT)
    submit_btn_checkout.click()

    firstname_field = driver.find_element(*FIRST_NAME)
    firstname_field.clear()
    firstname_field.send_keys(firstname)

    lastname_field = wait.until(EC.visibility_of_element_located(LAST_NAME))
    lastname_field.clear()
    lastname_field.send_keys(lastname)

    postalcode_field = driver.find_element(*POSTAL_CODE)
    postalcode_field.clear()
    postalcode_field.send_keys(postalcode)
    
    submit_btn_continue = driver.find_element(*CONTINUE_BUTTON)
    submit_btn_continue.click()
    
    submit_btn_finish = driver.find_element(*FINISH_BUTTON)
    submit_btn_finish.click()
    time.sleep(2)

# --- Тесты ---
@pytest.mark.parametrize(
    "login,password, firstname, lastname, postalcode",
    [
        ("standard_user", "secret_sauce", "roman", "zelenokhat", "123"),      # Успешная авторизация, покупка 1 товара, успешное заполнение формы
    ],
    ids=[
        "valid_credentials"
    ]
)

#Прогоняем тесты с полученными параметрами на Веб-интерфейсе, разделяяя их на положительный и отрицательные
def test_login(driver, wait, login, password, firstname, lastname, postalcode):
    driver.get("https://www.saucedemo.com/")  # URL адреса сайта
    fill_login_form(driver, wait, login, password, firstname, lastname, postalcode)

    if True:
        # Проверяем, что вход успешен (появился элемент профиля/личный кабинет)
        wait.until(EC.visibility_of_element_located(COMPLETE_OUTPUT))
        assert True, "Успешная покупка"
    else:
        assert False, "Неудачная покупка"