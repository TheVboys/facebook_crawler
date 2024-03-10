# group.py
from const import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from datetime import datetime, timedelta
from time import sleep
from typing import List
from tqdm import tqdm
import random


class Group:
    def __init__(self, browser):
        """
        Initialize Group object.

        Args:
            browser: Selenium WebDriver instance.
        """
        self.browser = browser

        self.group_name = None
        self.group_member = None
        self.group_url = None


    def get_url_from_members(self, url_group: str, max_user=0, time_limit=0) -> List[str]:
        """
        Extract user URLs from group members.

        Args:
            url_group (str): URL of the group.
            max_user (int, optional): Maximum number of users to crawl. Defaults to 0.
            time_limit (int, optional): Time limit for crawling in seconds. Defaults to 0.

        Returns:
            list: List of user URLs.
        """
        self.group_url = url_group
        self.browser.get(url_group+'/members')
        self.browser.execute_script("document.body.style.zoom='10%'")
        self.group_name = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, Xpath_group_name))).text
        self.group_member = int(WebDriverWait(self.browser, 2).until(EC.presence_of_element_located((By.XPATH, Xpath_group_max_members[:-5]))).text[4:])
        
        if max_user == 0:
            max_user = self.group_member
            print(f"Current members of {self.group_name}: {self.group_member}")
        else:
            print(f"Start Crawling User from Group: {self.group_name}")

        start_time = datetime.now()
        
        members = []
        last_members_len = len(members)
        count = 0
        while len(members) < max_user:   
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(random.randint(3, 5)) 
            members = WebDriverWait(self.browser, 2).until(EC.presence_of_all_elements_located((By.XPATH, xPath_group_members)))

            print(f'==={len(members)}/{max_user}')

            if len(members) == last_members_len:
                count+=1
                if count == 3:
                    print(f'Error: Cannot get more. Only get {len(members)} users in this session.')
                    break
            else:  count=0
            
            last_members_len = len(members)
            if time_limit != 0 and datetime.now() - start_time > timedelta(seconds=time_limit): 
                print(f'Reach time limit. Get {len(members)} users in this session.')
                max_user = len(members)  # set max_user to current member list
                break

        url_from_group = []
        for member in tqdm(members[:max_user]):
            try:
                user_url = WebDriverWait(member, 2).until(EC.presence_of_element_located((By.XPATH, xPath_group_user_url))).get_attribute("href")
                user_url = base_url + user_url.split('/')[-2]
                url_from_group.append(user_url)
            except:
                pass

        return url_from_group
