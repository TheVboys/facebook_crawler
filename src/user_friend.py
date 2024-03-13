from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from src.const import *
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

class UserFriend:

    def __init__(self, driver):
        self.driver = driver

    def _move_to_friendtab(self, url: str):
        url_suffix = '&sk=friends' if 'id=' in url else '/friends'
        self.driver.get(url + url_suffix)
        self.driver.execute_script("document.body.style.zoom='10%'")

    def _check_public(self, xpath: str) -> bool:

        hrefAtt = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath))).get_attribute("href")
        match = re.search(r'friends_all$', str(hrefAtt))

        return True if match else False

    def _loop_friends_list(self, css_attr: str):

        return self.driver.find_elements(By.CSS_SELECTOR, css_attr)

    def _is_end_of_friend_tab(self) -> int:

        try:
            end_tags = self.driver.find_elements(By.XPATH, endTabXpath)

        except:
            end_tags = []

        return len(end_tags) > 0

    def _get_friends_list(self, max_friends: int):

        numOfLoadedFriends = len(self._loop_friends_list(friendAttr))
        friendCount = 0
        limit = 0
        print(max_friends)


        while True:
            self.driver.execute_script(scrollFriendTab)
            try:
                WebDriverWait(self.driver, 2).until(lambda driver: len(self._loop_friends_list(friendAttr)) > numOfLoadedFriends)
                numOfLoadedFriends = len(self._loop_friends_list(friendAttr))  
                friendCount = len(self.driver.find_elements(By.CSS_SELECTOR, friendAttr))
               
                if friendCount >= max_friends:
                    print("Maximum number of friends reached, stopping...", limit)
                    break
        
            except TimeoutException:
                if self._is_end_of_friend_tab():
                    print("No more friend to receive, stopping...")
                    break  
                print("Getting TimeoutException, please check your FUCKING internet connection, we will retrying...")

        urlList = [friend.get_attribute("href") for friend in self.driver.find_elements(By.CSS_SELECTOR, friendAttr)]
 
        return urlList[2:max_friends+2] if max_friends < len(urlList)-2 else urlList[2:]

