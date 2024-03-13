from selenium.webdriver.common.by import By


def login(driver, username, password):
    """
    Log in to a website using the provided WebDriver instance.

    Args:
        driver: WebDriver instance.
        username (str): Username or email for login.
        password (str): Password for login.
    """
    try:
        user_name_field = driver.find_element(By.XPATH, "//input[@name='email']").send_keys(username)
        password_field = driver.find_element(By.XPATH, "//input[@name='pass']").send_keys(password)
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']").click()
        print('Success Login')
    except:
        print('Error Login')


