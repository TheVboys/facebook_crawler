from selenium.webdriver.common.by import By
from src.const import *
from datetime import datetime
now = datetime.now().strftime('%H:%M:%S')

def login(driver, username, password):
    """
    Log in to a website using the provided WebDriver instance.

    Args:
        driver: WebDriver instance.
        username (str): Username or email for login.
        password (str): Password for login.
    """
    driver.get(base_url)
    try:
        driver.find_element(By.XPATH, "//input[@name='email']").send_keys(username)
        driver.find_element(By.XPATH, "//input[@name='pass']").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        print(f'{now} utils.Login: Login Successfull')
    except:
        print(f'{now} utils.Login: Login Error')


