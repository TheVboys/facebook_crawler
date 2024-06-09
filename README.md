# facebook_crawler
This project aims to build a comprehensive database to support student recruitment, specifically focusing on high school students using Facebook who show tendencies to enroll in fields related to the Faculty of Engineering and Technology.

**Objectives**
- Collect Fanpage List: Gather a list of fanpages from 27 high schools.
- Web Crawler Development: Develop a web crawler to collect information about users interacting with these fanpages.
- Data Cleaning and Standardization: Clean and standardize the collected data.

## System Requirements

```python
Google Chrome: 119.0.6045.160 (64 bit) (cohort: Stable)
ChromeDriver: 119.0.6045.105 
python=3.9
```

👉 Find Chrome driver 119 [here](https://googlechromelabs.github.io/chrome-for-testing/).

**Note:** It is essential to use a Chrome Driver version that matches your Google Chrome browser. To check your browser version, navigate to `chrome://version` in your browser. Ensure compatibility by downloading the appropriate Chrome Driver version [here](https://chromedriver.chromium.org/downloads).

## System flows

<p align="center">
    
<img src="https://github.com/TheVboys/facebook_crawler/blob/main/assest/crawl_flow.png"  alt="System flow">

</p>

## Installation

1. Clone repo   
```bash
git clone https://github.com/TheVboys/facebook_crawler
```
2. cd to the folder
```bash
cd facebook_crawler
```
3. Intall dependencies
```bash
pip install -r requirements.txt
```

## Usage

### 1. Crawl Fanpage reactors

1. Put the dataset contain fanage link at folder `dataset` with name `fanpages.csv`
2. Execute this command in terminal
```bash
python src/fanpage_bot.py
```
3. When the crawling process is finished, `reactors.csv` will be created and contain the extracted data.

### 2. Craw Group members

```python
import src.group
import pandas as pd

group_crawler = group.Group(browser=browser)

for url_group in group_urls:
    member_urls = group_crawler.get_url_from_members(url_group, common=True, max_user=20)

    file_name = '../datasets/user_from_group_2.csv'
    existing_df = pd.read_csv(file_name)

    data = {
        'group': [group_crawler.group_name] * len(member_urls),
        'member_url': member_urls
    }
    new_data = pd.DataFrame(data)
    updated_df = pd.concat([existing_df, new_data], ignore_index=True)

    # Save the updated DataFrame back to the CSV file
    updated_df.to_csv(file_name, index=False)
```

### 3. Crawl user profile

```python
import pandas as pd
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from utils.login import login
import src.user_profile

def setup_browser():
    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")
    option.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
    return webdriver.Chrome(options=option)

def initialize_crawler(browser):
    return user_profile.UserInfo(browser)

def login_to_facebook(browser, username, password):
    browser.get("https://www.facebook.com/")
    login(browser, username, password)

def get_user_data(user_inf_crawler, url, group):
    name, basic_inf, school, locate = user_inf_crawler.get_user_info(url)
    raw_data = {'url': url, 'name': name, 'group': group, **basic_inf, **school, **locate}
    return raw_data

def process_and_save_data(existing_df, data, save_path):
    columns = existing_df.columns
    data = {k.replace(' ', ''): v for k, v in data.items()}
    data = {k: (v.replace('Studied at ', '').replace('Went to ', '') if k in ['Highschool', 'College'] else v) for k, v in data.items()}
    existing_df = pd.concat([existing_df, pd.DataFrame([{col: data.get(col, None) for col in columns}])], ignore_index=True)
    existing_df.to_csv(save_path, index=False)
    return existing_df

def get_members():
    browser = setup_browser()
    user_inf_crawler = initialize_crawler(browser)
    login_to_facebook(browser, "your_username", "your_password")
    
    save_path = '../datasets/user_info_from_group.csv'
    df = pd.read_csv('../datasets/data.csv')
    existing_df = pd.read_csv(save_path)
    count = existing_df.shape[0]
    
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processing rows"):
        url, group = row['member_url'], row['group']
        try:
            raw_data = get_user_data(user_inf_crawler, url, group)
            print(raw_data)
            existing_df = process_and_save_data(existing_df, raw_data, save_path)
            count += 1
            if count % 5 == 0:
                print('save', count)
        except Exception as e:
            print(f"Error processing {url}: {e}")
            continue

get_members()
```

### 4. Get user friends

```python
from src.user_friend import UserFriend

F = UserFriend()
F.get_friends_list()
``` 

