from selenium.webdriver.common.by import By
import time
from src.const import *

def login(driver, username, password):
    """
    Log in to a website using the provided WebDriver instance.

    Args:
        driver: WebDriver instance.
        username (str): Username or email for login.
        password (str): Password for login.
    """
    driver.get(base_url)
    driver.maximize_window()
    user_name = driver.find_element(By.XPATH, xPathUsername)
    user_name.send_keys(username)
    pass_word = driver.find_element(By.XPATH, xPathPassword)
    pass_word.send_keys(password)
    log_in_button = driver.find_element(By.XPATH, xPathSubmit).click()
    time.sleep(5)
    print('Success Login')



