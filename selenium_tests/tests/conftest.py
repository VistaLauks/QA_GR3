import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


# Фикстура для запуска и закрытия браузера
@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()

# Ожидание прогрузки браузера, если плохое соединение с интернетом или перегрузка
@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 10)