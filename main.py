from src.user_friend import UserFriend
from selenium import webdriver
from src.utils.login import login
from selenium.webdriver.chrome.options import Options
from src.const import *
import pandas as pd
import time
option = Options()
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
option.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)

PATH = "extensions/chromedriver.exe"
driver = webdriver.Chrome(options=option)

login(driver, "yelan482@gmail.com", "Linhcute542002")
time.sleep(5)

us = UserFriend(driver)
us._move_to_friendtab("https://www.facebook.com/profile.php?id=100093944898219")
checkvar = us._check_public(friendXPath)
if checkvar:
    friendUrlList = us._get_friends_list(29)
    df = pd.DataFrame(friendUrlList)
    df.to_csv('result.csv')