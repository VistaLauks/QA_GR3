from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def demo_login():
    # Запуск драйвера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get("https://www.saucedemo.com/")

    print("\n===== ЛОКАТОРЫ НА SAUCEDEMO =====")

    # 1. По ID — поле username
    username = driver.find_element(By.ID, "user-name")
    username.send_keys("standard_user")
    print("✅ По ID: поле username найдено")

    # 2. По ID — поле password
    password = driver.find_element(By.ID, "password")
    password.send_keys("secret_sauce")
    print("✅ По ID: поле password найдено")

    # 3. По ID — кнопка Login
    login_btn = driver.find_element(By.ID, "login-button")
    print(f"✅ По ID: кнопка '{login_btn.get_attribute('value')}' найдена")

    # 4. По классу — логотип
    logo = driver.find_element(By.CLASS_NAME, "login_logo")
    print(f"✅ По CLASS_NAME: логотип '{logo.text}'")

    # 5. По CSS — блок с тестовыми данными
    credentials = driver.find_element(By.CSS_SELECTOR, "#login_credentials")
    print(f"✅ По CSS: блок с данными найден")

    # Нажимаем кнопку Login
    login_btn.click()
    time.sleep(2)  # ждём загрузки страницы товаров

    # 6. Проверка — заголовок страницы товаров
    title = driver.find_element(By.CLASS_NAME, "title")
    print(f"✅ Заголовок страницы: '{title.text}'")

    # 7. По CSS — все товары
    items = driver.find_elements(By.CLASS_NAME, "inventory_item")
    print(f"✅ Найдено товаров: {len(items)}")

    # 8. По CSS — первый товар
    first_item = driver.find_element(By.CSS_SELECTOR, ".inventory_item:first-child")
    name = first_item.find_element(By.CLASS_NAME, "inventory_item_name")
    price = first_item.find_element(By.CLASS_NAME, "inventory_item_price")
    print(f"✅ Первый товар: '{name.text}' — {price.text}")

    # 9. По CSS — кнопка Add to cart у первого товара (исправлено)
    add_btn = first_item.find_element(By.CLASS_NAME, "btn_inventory")
    print(f"✅ По CSS (через первый товар): кнопка '{add_btn.text}'")

    # 10. Альтернативный вариант — через XPath (правильный синтаксис)
    # Находим кнопку у первого элемента с классом inventory_item
    add_btn_xpath = driver.find_element(By.XPATH, "(//div[@class='inventory_item'])[1]//button")
    print(f"✅ По XPath (правильный): кнопка '{add_btn_xpath.text}'")

    # Небольшая пауза, чтобы увидеть результат
    time.sleep(3)
    driver.quit()

if __name__ == "__main__":
    demo_login()