from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

def demo_login():
    # Запуск драйвера, чтобы страница загрузилась в режиме "Инконгито - это необходимо для защиты от уведомления Гугл, что ваш пароль раскрыт"
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()
    driver.get("https://www.saucedemo.com/")

    print("\n===== ЛОКАТОРЫ НА SAUCEDEMO =====")

    # 1. По ID — поле username, вводим значение visual_user
    username = driver.find_element(By.ID, "user-name")
    username.send_keys("visual_user")
    print("✅ По ID: поле username найдено")

    # 2. По ID — поле password, вводим значение secret_sauce
    password = driver.find_element(By.ID, "password")
    password.send_keys("secret_sauce")
    print("✅ По ID: поле password найдено")

    # 3. По ID — кнопка Login (только нахлждение кнопки)
    login_btn = driver.find_element(By.ID, "login-button")
    print(f"✅ По ID: кнопка '{login_btn.get_attribute('value')}' найдена")

    # 4. По классу — нахождение логинов учетных записей пользователей
    login = driver.find_element(By.CLASS_NAME, "login_credentials")
    print(f"✅ По CLASS_NAME: логины учетных записей '{login.text}'")

    # 5. По CSS — логотип
    credentials = driver.find_element(By.CSS_SELECTOR, "#root > div > div.login_logo")
    print(f"✅ По CSS: блок с данными найден")

    # Нажимаем кнопку Login
    login_btn.click()
    time.sleep(2)  # ждём загрузки страницы товаров

    # 6. Проверка — сортировка товара по алфавиту
    alfavit = driver.find_element(By.CLASS_NAME, "product_sort_container")
    print(f"✅ Сортировка по алфавиту: '{alfavit.text}'")

    # 7. По классу - сколько всего товаров
    items = driver.find_elements(By.CLASS_NAME, "inventory_item")
    print(f"✅ Найдено товаров: {len(items)}")

    # 8. По CSS — последний товар
    last_item = driver.find_element(By.CSS_SELECTOR, "#inventory_container > div > div:nth-child(6)")
    name = last_item.find_element(By.CSS_SELECTOR, "#inventory_container > div > div:nth-child(6) > div.inventory_item_description > div.inventory_item_label")
    price = last_item.find_element(By.CSS_SELECTOR, "#inventory_container > div > div:nth-child(6) > div.inventory_item_description > div.pricebar > div")
    print(f"✅ Первый товар: '{name.text}' — {price.text}")

    # 9. Через XPATH - Добавление посленего товара в корзину
    add_btn_xpath = driver.find_element(By.XPATH, "/html/body/div/div/div/div/div/div/div/div[6]/div[2]/div[2]/button")
    print(f"✅ По XPath: кнопка '{add_btn_xpath.text}'")

    # Добавляем товар
    add_btn_xpath.click()
    time.sleep(2)  # ждём загрузки товара в корзину

    # 10. Через XPATH - Открытие Корзины, чтобы посмотреть добавленный товар
    look_btn_xpath = driver.find_element(By.XPATH, "/html/body/div/div/div/header/div[1]/div[3]/a")
    print(f"✅ По XPath: кнопка '{look_btn_xpath.text}'")

    # Нажимаем корзинку
    look_btn_xpath.click()
    time.sleep(2)

    # Небольшая пауза, чтобы увидеть результат
    time.sleep(3)
    driver.quit()

if __name__ == "__main__":
    demo_login()