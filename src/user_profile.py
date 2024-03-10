from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from const import *

class UserInfo:
    """Class to represent a user profile."""

    def __init__(self, driver):
        """
        Initialize User instance with URL and WebDriver.

        Args:
            url (str): URL of the user's profile.
            driver: WebDriver instance.
        """
        self.driver = driver

    def get_user_info(self, url):
        self.url = url
        self.name, self.gender, self.year = self._get_basic_info()
        self.school_name = self._get_work_and_education()
        return self.name, self.gender, self.year, self.school_name

    def _get_element_text(self, xpath, wait=2, element=None):
        """
        Retrieve text content of an element using XPath.

        Args:
            xpath (str): XPath of the element.
            element: Web element to search within (optional).

        Returns:
            str: Text content of the element.
        """
        try:
            if element:
                return WebDriverWait(element, wait).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                ).text
            else:
                return WebDriverWait(self.driver, wait).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                ).text
        except:
            return None

    def _get_basic_info(self):
        """
        Retrieve basic information such as name, gender, and birth year.
        """
        url_suffix = '&sk=about_contact_and_basic_info' if 'id=' in self.url else '/about_contact_and_basic_info'
        self.driver.get(self.url + url_suffix)

        name = self._get_element_text(xPath_name)
        gender = self._get_element_text(xPath_gender)
        year = self._get_element_text(xPath_year)
        
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
                school_name = self._get_element_text(xPath_school_name, element=work_box)
                school_names.append(school_name)
        except:
            pass
        
        return school_names
