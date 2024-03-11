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

# Constants should be defined within the class or as module-level constants.
# I will assume these constants are defined elsewhere.

class UserFriend:

    def __init__(self, driver):
        """
        Constructor for UserFriend class.

        Args:
        - driver: Selenium WebDriver object.
        """
        self.driver = driver

    def _move_to_friendtab(self, url):
        """
        Moves to the friend tab of a user's profile.

        Args:
        - url: URL of the user's profile.
        """
        url_suffix = '&sk=friends' if 'id=' in url else '/friends'
        self.driver.get(url + url_suffix)
        self.driver.execute_script("document.body.style.zoom='10%'")

    def _check_public(self, path):
        """
        Checks if the friend list is public or private.

        Args:
        - path: XPath of the element indicating a friend's presence.

        Returns:
        - 'visible' if the friend list is visible.
        - 'invisible' if the friend list is invisible.
        """
        test_friend = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, path)))
        abc = test_friend.get_attribute("href")
        match = re.search(r'friends_all$', str(abc))
        return 'visible' if match else 'invisible'

    def _loop_friends_list(self, path):
        """
        Loops through the list of friends.

        Args:
        - path: CSS selector for the friend list.

        Returns:
        - List of Selenium WebElements representing friends.
        """
        return self.driver.find_elements(By.CSS_SELECTOR, path)

    def _get_friends_list(self):
        """
        Retrieves the list of friends.

        Returns:
        - List of URLs of friends' profiles.
        """
        num_of_loaded_friends = len(self._loop_friends_list(xPathFriends))
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                WebDriverWait(self.driver, 2).until(lambda driver: len(self._loop_friends_list(xPathFriends)) > num_of_loaded_friends)
                num_of_loaded_friends = len(self._loop_friends_list(xPathFriends))
            except TimeoutException:
                break  
        urlList = []
        my_friend = self.driver.find_elements(By.CSS_SELECTOR, xPathFriends)
        for friend in my_friend:
            url = friend.get_attribute("href")
            urlList.append(url)
        return urlList
