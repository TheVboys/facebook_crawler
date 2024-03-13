from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from const import *
from utils import get_element


class UserInfo:
    """Class to represent a user profile."""

    def __init__(self, browser):
        """
        Initialize User instance with URL and WebDriver.

        Args:
            driver: WebDriver instance.
        """
        self.browser = browser

    def get_user_info(self, url):
        self.url = url
        name, basic_info_dict = self._get_basic_info()
        school_name = self._get_work_and_education()
        places = self._place_lives()
        return name, basic_info_dict, school_name, places

    def _get_basic_info(self):
        """
        Retrieve basic information such as name, gender, and birth year.
        """
        url_suffix = '&sk=about_contact_and_basic_info' if 'id=' in self.url else '/about_contact_and_basic_info'
        self.browser.get(self.url + url_suffix)
        name = get_element.get_element(browser=self.browser, xpath=xPath_name).text
        contact_info_box = get_element.get_element_list(self.browser, '//div[@class = "xyamay9 xqmdsaz x1gan7if x1swvt13"]/div')
        
        try:
            key = get_element.get_element_list(self.browser, xpath=xPath_basic_inf['key'], element=contact_info_box[-1])
            value = get_element.get_element_list(self.browser, xpath=xPath_basic_inf['value'], element=contact_info_box[-1])
            basic_info_dict = {key[i].text:value[i].text  for i in range(len(key))}
        except:
            basic_info_dict = None
        return name.strip(), basic_info_dict


    def _get_work_and_education(self):
        """
        Retrieve work and education information.
        """
        url_suffix = '&sk=about_work_and_education' if 'id=' in self.url else '/about_work_and_education'
        self.browser.get(self.url + url_suffix)
        schools_inf = {}
        try:
            school_box_list = get_element.get_element_list(self.browser, xpath=xPath_schools)[1:]
            for school in school_box_list:
                try:
                    key = get_element.get_element(browser=self.browser, xpath=xPath_schools_inf['key'], element=school).text
                    value = get_element.get_element(browser=self.browser, xpath=xPath_schools_inf['value'], element=school).text
                    schools_inf[key] = value
                except:
                    pass
        except:
            pass
        return schools_inf

    def _place_lives(self):
        """
        Retrieve places information.
        """
        url_suffix = '&sk=about_places' if 'id=' in self.url else '/about_places'
        self.browser.get(self.url + url_suffix)
        places = get_element.get_element(browser=self.browser, xpath=xPath_places)
        try:
            key = get_element.get_element_list(self.browser, xpath=xPath_places_inf['key'], element=places)
            value = get_element.get_element_list(self.browser, xpath=xPath_places_inf['value'], element=places)
            places_info_dict = {key[i].text:value[i].text  for i in range(len(key))}
        except:
            places_info_dict = None
        return places_info_dict