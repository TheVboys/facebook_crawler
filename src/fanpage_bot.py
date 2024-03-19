from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from facebook_scraper import get_reactors

import os
import re
import pandas as pd
from time import sleep, time
import random
import csv
from datetime import datetime, timedelta

class GetUserFanpage:
    def __init__(self):
        
        #dataset
        self.df = pd.read_csv('./datasets/fanpages.csv')

        # webdriver
        driver_location = "extensions/chromedriver.exe"
        # binary_location = '/usr/bin/google-chrome' # remove this on windown

        # Options
        options = ChromeOptions()
        service = Service(executable_path=driver_location)
        # options.binary_location = binary_location # remove this on windown

        options.add_experimental_option("detach", True)
        options.add_argument("--disable-extensions")
        # options.add_argument("--headless")
        options.add_argument("--incognito")
        options.add_argument("--window-size=1920x1080")
        self.browser = Chrome(service=service, options=options)
        self.browser.maximize_window()
        self.actions = ActionChains(self.browser)

    def get_post_link(self, link):
        
        try:
            self.browser.get(link)
            sleep(random.randint(3, 5))
        except Exception as e: 
            print(f"An error occurred while try to reach '{link}'", str(e))
            return [], None
        
        try:
            self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div").click()
        except NoSuchElementException:
            sleep(5)
            try:
                self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div").click()
            except NoSuchElementException:
                pass
                
        sleep(random.randint(3, 5)) 
        try:
            fanpage_name = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[1]/div/div/span/h1").text
        except:
            fanpage_name = "NONE"

        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(random.randint(3,5))
        self.browser.execute_script("window.scrollTo(0, 1000);")

        post_link = []
        for i in range(1,50):
            try:
                # Hover 
                post = self.browser.find_element(By.XPATH,
                                            f"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div/div[{i}]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div[2]/div/div[2]/span/span/span[2]/span"
                                            )
                self.actions.move_to_element(post).perform()
                self.browser.execute_script("window.scrollTo(0, 1000);")
                a_tag = post.find_element(By.XPATH, ".//a")
                link = a_tag.get_attribute("href")
                link = re.sub(r"__cft__.*", "", link)
                print(link)
                post_link.append(link)
                sleep(2)
            except:
                self.browser.execute_script("window.scrollTo(0, 500);")
            if len(post_link) >= 15: break 
        print(f"{fanpage_name} done")

        return post_link, fanpage_name
    
    def get_all_post_from_fanpage(self, start=0):
        
        try:
            for i, link in enumerate(self.df["link"][start:]):
            
                user_links, fanpage_name = self.get_post_link(link)
                self.save_to_csv(user_links, fanpage_name, './datasets/post_fanpage.csv')
        
        except Exception as e: 
                print("An error occurred:", str(e))
                self.browser.quit()
                self.get_all_post_from_fanpage(start=i)    

        self.browser.quit()
        return
    
    def get_reactors(self):
        post_links = pd.read_csv("./datasets/post_fanpage.csv")
        

        for index, post in post_links.iterrows():
            link = post["post_links"]
            fanpage_name = post["fanpage"]

            links = []
            user_names = []
            post_id = self.extract_post_id(link)
            if post_id is not None:
                for reactors in get_reactors(post_id, cookies='./facebook_cookies.txt',
                                    options={"allow_extra_requests": True,
                                            "reactions": True, 'reactors': True},
                                    ):
                    links.append(reactors["link"])
                    user_names.append(reactors["name"])
                self.save_to_csv(links, fanpage_name, "./datasets/reactors.csv", "user_url")
        try:
            self.browser.quit()
        except:
            pass
        return
    
    def extract_post_id(self, url):
        # Define the regular expression pattern to match the post ID
        pattern = r"(?:story_fbid=|posts/|id=|videos/)([^/&?]+)"
        # Search for the pattern in the URL
        match = re.search(pattern, url)
        # If a match is found, extract the post ID
        if match:
            post_id = match.group(1)
            # Remove any trailing characters after the post ID
            post_id = post_id.split(":")[0]
            return post_id
        else:
            return None
        
    def save_to_csv(self, links, fanpage_names, filename, col1="post_links", col2="fanpage"):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        file_exists = os.path.isfile(filename)
        
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            # If the file doesn't exist, write the header
            if not file_exists:
                writer.writerow([col1, col2])
            # Write the links and fan page name to the file 
            for link in links:
                writer.writerow([link, fanpage_names])

# G = GetUserFanpage()
# G.get_all_post_from_fanpage()
# G.get_reactors()