from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from src.const import *
import pandas as pd

class UserFriend:

    def __init__(self, url, driver):
        self.url = url
        self.driver = driver

    def _move_to_friendtab(self):
        self.driver.get(self.url)
        friendsTab = self.driver.find_element(By.XPATH,"//span[text()='Friends']")
        friendsTab.click()

    def _check_public(self, path):
        time.sleep(5)
        self.driver.execute_script("window.scrollTo(0, 500)")
        test_friend = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, path)))
        abc = test_friend.get_attribute("href")
        match = re.search(r'friends_all$', str(abc))
        if match is not None:
            return 'visible'
        else:
            return 'invisible'

    def _loop_friends_list(self, path):
        return self.driver.find_elements(By.CSS_SELECTOR, path)

    def _get_friends_list(self):
        num_of_loaded_friends = len(self._loop_friends_list(xPathFriends))
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                WebDriverWait(self.driver, 2).until(lambda driver: len(self._loop_friends_list(xPathFriends)) > num_of_loaded_friends)
                num_of_loaded_friends = len(self._loop_friends_list(xPathFriends))
            except TimeoutException:
                break  # no more friends loaded
        friendsList = []
        urlList = []
        my_friend = self.driver.find_elements(By.CSS_SELECTOR, xPathFriends)
        for friend in my_friend:
            friendsList.append(friend.text)
            url = friend.get_attribute("href")
            urlList.append(url)
            print(friend.text, url)
        