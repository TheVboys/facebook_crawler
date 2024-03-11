from src.user_friend import UserFriend
from selenium import webdriver
from src.utils.login import login
from selenium.webdriver.chrome.options import Options
from src.const import *


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

us = UserFriend("https://www.facebook.com/profile.php?id=100093944898219", driver)
us._move_to_friendtab()
checkvar = us._check_public(arialLabelFriendTab)
if checkvar == 'visible':
    us._get_friends_list()