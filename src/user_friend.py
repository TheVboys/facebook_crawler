#Webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import selenium
from datetime import datetime, timedelta

#Local Package
from src.const import *

#Other Package
import re
import pandas as pd


class UserFriend:
    """Class to scrape user's friends from a social media platform."""

    def __init__(self, driver):
        """Initialize UserFriendScraper with a Selenium WebDriver."""
        self.driver = driver


    def _open_friend_tab(self, url: str):
        """
        Open the friend tab of the user's profile.

        Args:
            url (str): The URL of the user's profile.
        """
        url_suffix = '&sk=friends' if 'id=' in url else '/friends'
        self.driver.get(url + url_suffix)
        self.driver.execute_script("document.body.style.zoom='10%'")


    def _is_visible(self, xpath: str) -> bool:
        """
        Check if user's profile able to show friends list.

        Returns:
            bool: True if it's visible, False otherwise.
        """
        try:
            hrefAtt = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath))).get_attribute("href")
            match = re.search(r'friends_all$', str(hrefAtt))
        except Exception as e:
            now = datetime.now().strftime('%H:%M:%S')
            print(f'{now} src.GetFriend: Getting An Error, Passing to the the next URL...')
            match = False
        return True if match else False


    def _is_end_of_friend_tab(self) -> bool:
        """
        Check if it's the end of the friend list page.

        Returns:
            bool: True if it's the end of the friend list, False otherwise.
        """
        try:
            end_tags = self.driver.find_elements(By.XPATH, endTabXpath)
        except:
            end_tags = []
        return len(end_tags) > 0


    def _loop_friends_list(self, css_attr: str):
        """Get the WebElements of the user's friends"""
        return self.driver.find_elements(By.CSS_SELECTOR, css_attr)



    def _get_friends_list(self, max_urls = 0, time_limit = 0):
        """
        Get the URLs of the user's friends.

        Returns:
            list: List of URLs of the user's friends.
        """
        numOfLoadedFriends = len(self._loop_friends_list(friendAttr))
        friendCount = 0
        start_time = datetime.now()

        while True:
            self.driver.execute_script(scrollFriendTab)
            try:
                WebDriverWait(self.driver, 2).until(lambda driver: len(self._loop_friends_list(friendAttr)) > numOfLoadedFriends)
                numOfLoadedFriends = len(self._loop_friends_list(friendAttr))  
                friendCount = len(self.driver.find_elements(By.CSS_SELECTOR, friendAttr))
                if max_urls > 0 and friendCount >= max_urls:
                    now = datetime.now().strftime('%H:%M:%S')
                    print(f"{now} src.GetFriend: Maximum number of friends reached, Stopping...")
                    break
                if time_limit > 0 and datetime.now() - start_time > timedelta(seconds=time_limit): 
                    now = datetime.now().strftime('%H:%M:%S')
                    print(f"{now} src.GetFriend: Time limit reached, Stopping...")
                    max_urls = friendCount
                    break
            except TimeoutException:
                if self._is_end_of_friend_tab():
                    now = datetime.now().strftime('%H:%M:%S')
                    print(f"{now} src.GetFriend: No more friend to receive, Stopping...")
                    break  
                now = datetime.now().strftime('%H:%M:%S')
                print(f"{now} src.GetFriend: Getting TimeoutException, please check your internet connection, Retrying...")
        urlList = [friend.get_attribute("href") for friend in self.driver.find_elements(By.CSS_SELECTOR, friendAttr)]
        return urlList[2: max_urls+2] if (max_urls < (len(urlList)-2)) and (max_urls > 0) else urlList[2:]

