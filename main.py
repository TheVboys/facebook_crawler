from src.user_friend import UserFriend
from src.utils.db import DatabaseClient
from src.fanpage_bot import GetUserFanpage
from src.user_profile import UserInfo
from src.group import Group
from selenium import webdriver
from src.utils.login import login
from selenium.webdriver.chrome.options import Options
from src.const import *
import pandas as pd
import time
from datetime import datetime
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

friendClient = UserFriend(driver)
groupClient = Group(driver)
starterUrl = pd.read_csv(filePath)['url'].to_list()


def get_friend(url_list, check_point = 0):
    result = []
    for url in url_list:
        friendClient._open_friend_tab(url)
        isVisible = friendClient._is_visible(friendXPath)
        if isVisible:
            friendUrlList = friendClient._get_friends_list(100)
            for elem in friendUrlList:
                result.append(elem)
            if len(result) >= check_point:
                DatabaseClient(mongodb_uri)._insert_url(result, "friend")
                result = []
                now = datetime.now().strftime('%H:%M:%S')
                print(f"{now} main: Finished Insert Checkpoint")

get_friend(starterUrl, 200)
now = datetime.now().strftime('%H:%M:%S')
print(f"{now} main: Finished")