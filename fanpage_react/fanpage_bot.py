from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

import os
import re
import pandas as pd
from time import sleep, time
import random
import csv
from datetime import datetime, timedelta

class GET_USER_FFANPAGE:
    def __init__(self):
        
        #dataset
        self.df = pd.read_csv('./datasets/fanpages.csv')

        # webdriver
        driver_location = '/usr/bin/chromedriver'
        binary_location = '/usr/bin/google-chrome' # remove this on windown

        self.username = "Buithingan011195@gmail.com" #"yelan482@gmail.com" # "lthcolab@gmail.com" # "lth2112002@gmail.com" #
        self.password = "iubele"#"Linhcute542002" # "Huet123" # "Baoanh123" #
        
        # Options
        options = ChromeOptions()
        service = Service(executable_path=driver_location)
        options.binary_location = binary_location # remove this on windown

        options.add_experimental_option("detach", True)
        options.add_argument("--disable-extensions")
        # options.add_argument("--headless")
        options.add_argument("--incognito")
        options.add_argument("--window-size=1920x1080")
        self.browser = Chrome(service=service, options=options)
        self.browser.maximize_window()
        self.actions = ActionChains(self.browser)

    def login(self):

        self.browser.get("https://www.facebook.com/")
        assert "Facebook" in self.browser.title
        elem = self.browser.find_element(By.ID, "email")
        elem.send_keys(self.username)
        elem = self.browser.find_element(By.ID, "pass")
        elem.send_keys(self.password)

        self.browser.find_element(By.NAME, "login").click()
        sleep(random.randint(3, 5))

        return

    def get_user_link(self, link):
        
        try:
            self.browser.get(link)
        except Exception as e: 
            print(f"An error occurred while try to reach '{link}'", str(e))
            return [], None
        
        sleep(random.randint(3, 5)) 
        fanpage_name = self.browser.find_element(By.XPATH, "//div[@class='x1e56ztr x1xmf6yo']").text
        print(f"Crawling Fanpage: {fanpage_name}")
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        user_links = []
        sleep(random.randint(3, 5)) 

        start_time = datetime.now()
        all_post_react = self.browser.find_elements(By.XPATH, "//span[@class='xt0b8zv x2bj2ny xrbpyxo xl423tq']")

        while True:
            all_post_react = self.browser.find_elements(By.XPATH, "//span[@class='xt0b8zv x2bj2ny xrbpyxo xl423tq']")
            if len(all_post_react) < 15: 
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(random.randint(2,4))
                if datetime.now() - start_time > timedelta(seconds=30):
                    break   
            else: break

        print(len(all_post_react))
        post_range = 8 if 8 < len(all_post_react) else len(all_post_react)

        if post_range == 0: 
            print(f"{fanpage_name} found no post")  
            return user_links , fanpage_name
        
        # Scroll back to position 1000
        self.browser.execute_script("window.scrollTo(0, 1000);")

        for p in range(1,post_range):
            print("crawling post:", p)
            post_react = all_post_react[p]
            self.actions.move_to_element(post_react).perform()
            post_react.click()
            sleep(random.randint(3, 4))
            
            last_react_user = None
            start_time = time()
            last_a_tag = None
            a_tags = []
            while last_react_user is None:
                try:
                    last_react_user = self.browser.find_element(
                        By.XPATH,
                        f"/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[1]/div[{post_react.text}]/div/div"
                    )
                except:

                    popup = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]")
                    
                    try:                        
                        a_tags = popup.find_elements(By.XPATH, ".//a")
                    
                        print("a",len(a_tags))
                        if a_tags[-1] != last_a_tag:
                            start_time = time()
                        elif len(a_tags) >= 150: # set limit react user to 150
                            break
                        elif a_tags[-1] == last_a_tag and time() - start_time > 10:
                            break 

                        # Get the last <a> tag
                        last_a_tag = a_tags[-1]
                        # Scroll the last <a> tag into view
                        # self.browser.execute_script("arguments[0].scrollIntoView(true);", last_a_tag) 
                        self.browser.execute_script("document.body.style.transition = 'scroll-behavior 2s ease';")
                        self.browser.execute_script("arguments[0].scrollIntoView(true);", last_a_tag)

                        # push transition back
                        self.browser.execute_script("document.body.style.transition = '';")
                        sleep(random.randint(3,5))
                    except: break

            # a_tags = popup.find_elements(By.XPATH, ".//a")
            try:
                for a in a_tags:
                    link = a.get_attribute("href")
                    link = re.sub(r"__cft__.*", "", link)
                    user_links.append(link)
            except: 
                print("No react in this post")
            
            # close_element
            self.browser.find_element(
                By.XPATH,
                "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[2]/div",
            ).click()
            sleep(random.randint(2, 5))

        print(f"{fanpage_name} done")

        return user_links, fanpage_name
    
    def get_all_user_from_fanpage(self, start=0):
        self.login()
        try:
            for i, link in enumerate(self.df["link"][start:]):
            
                user_links, fanpage_name = self.get_user_link(link)
                self.save_user_links_to_csv(user_links, fanpage_name, './datasets/user_from_fanpage.csv')
        
        except Exception as e: 
                print("An error occurred:", str(e))
                self.browser.quit()
                self.get_all_user_from_fanpage(start=i)    

        self.browser.quit()
        return
    
    def save_user_links_to_csv(self, links, fanpage_name, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        file_exists = os.path.isfile(filename)
        
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            # If the file doesn't exist, write the header
            if not file_exists:
                writer.writerow(['user_link', 'fanpage'])
            # Write the links and fan page name to the file
            for link in links:
                writer.writerow([link, fanpage_name])

G = GET_USER_FFANPAGE()
G.get_all_user_from_fanpage()