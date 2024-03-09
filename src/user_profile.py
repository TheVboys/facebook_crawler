from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

xPath_name = '//span[@class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x14qwyeo xw06pyt x579bpy xjkpybl x1xlr1w8 xzsf02u x1yc453h"]/h1[@class = "x1heor9g x1qlqyl8 x1pd3egz x1a2a7pz"]'
xPath_gender = "//div[@class='xyamay9 xqmdsaz x1gan7if x1swvt13']/div[3]/div/div[2]/div/div/div[2]/div/div/div/div/div[1]/span"
xPath_year = "//div[@class = 'x1hq5gj4']/../div[3]/div/div/div[2]/div[2]/div/div/div/div/span"
xPath_schools = "//div[@class = 'xyamay9 xqmdsaz x1gan7if x1swvt13']/div"
xPath_school_name = ".//span[@class = 'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u']"

class UserInfo:
    """Class to represent a user profile."""

    def __init__(self, url, driver):
        """
        Initialize User instance with URL and WebDriver.

        Args:
            url (str): URL of the user's profile.
            driver: WebDriver instance.
        """
        self.url = url
        self.driver = driver
        self.name, self.gender, self.year = self._get_basic_info()
        self.school_name = self._get_work_and_education()

    def _get_basic_info(self):
        """
        Retrieve basic information such as name, gender, and birth year.
        """
        url_suffix = '&sk=about_contact_and_basic_info' if 'id=' in self.url else '/about_contact_and_basic_info'
        self.driver.get(self.url + url_suffix)

        name = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, xPath_name))
        ).text

        try:
            gender = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.XPATH, xPath_gender))
            ).text
        except:
            gender = None

        try:
            year = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.XPATH, xPath_year))
            ).text
        except:
            year = None
        
        return name, gender, year

    def _get_work_and_education(self):
        """
        Retrieve work and education information.
        """
        url_suffix = '&sk=about_work_and_education' if 'id=' in self.url else '/about_work_and_education'
        self.driver.get(self.url + url_suffix)

        school_names = []
        try:
            work_box_list = WebDriverWait(self.driver, 2).until(
                EC.presence_of_all_elements_located((By.XPATH, xPath_schools))
                )[1:]  # skip 1st element
            for work_box in work_box_list:
                try:
                    school_name = WebDriverWait(work_box, 2).until(
                        EC.presence_of_element_located((By.XPATH, xPath_school_name))
                    ).text
                    school_names.append(school_name)
                except:
                    pass
        except:
            pass
        
        return school_names
