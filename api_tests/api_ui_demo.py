import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def demo_api_ui_integration():
    print("\n===== ИНТЕГРАЦИЯ API И UI =====")

    # -------- 1. API: получаем данные --------
    print("1. Запрос к API...")
    resp = requests.get("https://jsonplaceholder.typicode.com/users/1")
    if resp.status_code != 200:
        print("❌ API не отвечает")
        return
    user = resp.json()
    print(f"   ✅ Получен пользователь: {user['name']}, email: {user['email']}")

    # -------- 2. UI: используем email для логина --------
    print("2. Открываем SauceDemo...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get("https://www.saucedemo.com/")

    # Вводим email из API (он не подойдёт, но показываем связку)
    driver.find_element(By.ID, "user-name").send_keys(user['email'])
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)

    # -------- 3. Проверяем результат --------
    print("3. Проверка результата...")
    try:
        # Если логин не удался — будет сообщение об ошибке
        error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        print(f"   ❌ Ошибка: {error.text.strip()}")
    except:
        title = driver.find_element(By.CLASS_NAME, "title")
        print(f"   ✅ Успех: '{title.text}'")

    time.sleep(2)
    driver.quit()

if __name__ == "__main__":
    demo_api_ui_integration()