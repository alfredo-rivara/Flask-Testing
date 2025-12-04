import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="module")
def driver():
    #Conectar al contenedor de Selenium (Chrome)
    chrome_options = Options()

    driver = webdriver.Remote(
        command_executor="http://localhost:4444/wd/hub",
        options=chrome_options
    )

    #Espera elementos
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_home_page_content(driver):
    url = "http://127.0.0.1:5000"
    print(f"Navigating to {url}")
    driver.get(url)

    #Capturar ID
    heading = driver.find_element(By.ID, "welcome-message")

    #QA check
    assert heading.text == "Hola! Bienvenido QA Testing de Flask"
    print("Test exitoso")
