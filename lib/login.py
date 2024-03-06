import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from lib.get_friend import .
import getpass
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import os
from dotenv import load_dotenv

option = Options()
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
option.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)
PATH = "extensions/chromedriver.exe"
driver = webdriver.Chrome(options=option)
driver.get("https://www.facebook.com/")
driver.maximize_window()

load_dotenv()

user_name = driver.find_element(By.XPATH,"//input[@name='email']")
user_name.send_keys(os.environ.get("email"))
password = driver.find_element(By.XPATH,"//input[@name='pass']")
password.send_keys(os.environ.get("password"))

log_in_button = driver.find_element(By.XPATH,"//button[@type='submit']")
log_in_button.click()