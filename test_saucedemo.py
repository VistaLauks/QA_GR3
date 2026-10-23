from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pytest


# ============================================================
# 1. ФИКСТУРЫ
# ============================================================

@pytest.fixture(scope="function")
def driver():
    """Фикстура: запуск и закрытие браузера (режим инкогнито)"""
    options = Options()
    options.add_argument("--incognito")  # ← Главное изменение!

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()


@pytest.fixture
def logged_in_driver(driver):
    """Фикстура: авторизованный пользователь"""
    driver.find_element(By.ID, "user-name").send_keys("error_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list")))
    return driver


# ============================================================
# 2. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================

def get_cart_badge_count(driver):
    """Возвращает количество товаров в корзине"""
    try:
        badge = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
        )
        return int(badge.text)
    except:
        return 0


def open_cart(driver):
    """Открывает корзину"""
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "cart_list")))
    time.sleep(0.5)


def remove_all_items_from_cart(driver):
    """Удаляет все товары из корзины"""
    remove_buttons = driver.find_elements(By.CSS_SELECTOR, ".cart_button")
    for btn in remove_buttons:
        if "Remove" in btn.text:
            btn.click()
            time.sleep(0.3)


def clear_cart_before_test(driver):
    """Очищает корзину перед тестом"""
    badge = get_cart_badge_count(driver)
    if badge > 0:
        open_cart(driver)
        remove_all_items_from_cart(driver)
        driver.find_element(By.ID, "continue-shopping").click()
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list")))
        time.sleep(0.5)


def fill_checkout_form(driver, first_name, last_name, zip_code):
    """Заполняет форму оформления заказа"""
    driver.find_element(By.ID, "first-name").send_keys(first_name)
    driver.find_element(By.ID, "last-name").send_keys(last_name)
    driver.find_element(By.ID, "postal-code").send_keys(zip_code)


# ============================================================
# 3. ТЕСТЫ
# ============================================================

# ---------- ТЕСТ 1: УСПЕШНАЯ ПОКУПКА ----------
@pytest.mark.smoke
@pytest.mark.regression
def test_successful_purchase(logged_in_driver):
    driver = logged_in_driver
    clear_cart_before_test(driver)

    # Добавляем товар
    add_btn = driver.find_element(By.CLASS_NAME, "btn_inventory")
    add_btn.click()
    time.sleep(0.5)
    assert get_cart_badge_count(driver) == 1

    # Переход в корзину
    open_cart(driver)

    cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(cart_items) == 1

    # Оформление заказа
    driver.find_element(By.ID, "checkout").click()
    WebDriverWait(driver, 5).until(EC.url_contains("checkout-step-one"))

    fill_checkout_form(driver, "Иван", "Петров", "123456")
    driver.find_element(By.ID, "continue").click()
    WebDriverWait(driver, 5).until(EC.url_contains("checkout-step-two"))

    driver.find_element(By.ID, "finish").click()

    success_msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
    ).text
    assert success_msg == "Thank you for your order!"
    print("✅ Успешная покупка пройдена")


# ---------- ТЕСТ 2: ОЧИЩЕНИЕ КОРЗИНЫ ----------
@pytest.mark.regression
def test_clear_cart(logged_in_driver):
    driver = logged_in_driver
    clear_cart_before_test(driver)

    # Добавляем 3 товара
    add_buttons = driver.find_elements(By.CLASS_NAME, "btn_inventory")
    count = 0
    for i in range(min(3, len(add_buttons))):
        add_buttons[i].click()
        count += 1
        time.sleep(0.5)
        WebDriverWait(driver, 5).until(
            lambda d: get_cart_badge_count(d) == count,
            f"Счётчик не обновился до {count}"
        )

    open_cart(driver)

    cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(cart_items) == count

    # Удаляем все товары
    remove_all_items_from_cart(driver)

    cart_items_after = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(cart_items_after) == 0

    try:
        driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert False, "Счётчик должен исчезнуть"
    except:
        pass

    print("✅ Очистка корзины пройдена")


# ---------- ТЕСТ 3: НЕУСПЕШНАЯ АВТОРИЗАЦИЯ ----------
@pytest.mark.smoke
@pytest.mark.regression
def test_unsuccessful_login(driver):
    driver.find_element(By.ID, "user-name").send_keys("invalid_user")
    driver.find_element(By.ID, "password").send_keys("invalid_pass")
    driver.find_element(By.ID, "login-button").click()

    error = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
    )
    expected = "Epic sadface: Username and password do not match any user in this service"
    assert error.text == expected
    assert "saucedemo.com" in driver.current_url
    print("✅ Неуспешная авторизация пройдена")


# ---------- ТЕСТ 4: ВЫХОД ИЗ СИСТЕМЫ ----------
@pytest.mark.regression
def test_logout(logged_in_driver):
    driver = logged_in_driver

    driver.find_element(By.ID, "react-burger-menu-btn").click()
    time.sleep(0.5)

    logout_btn = driver.find_element(By.ID, "logout_sidebar_link")
    ActionChains(driver).move_to_element(logout_btn).click().perform()

    username_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )
    assert username_field.is_displayed()
    assert "inventory" not in driver.current_url
    print("✅ Выход из системы пройден")


# ============================================================
# 4. ЗАПУСК
# ============================================================
if __name__ == "__main__":
    pytest.main(["-v", "--tb=short", __file__])