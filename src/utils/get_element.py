from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from typing import List

def get_element(browser, xpath, wait=2, element=None):
    """
    Retrieve content of an element using XPath.

    Args:
        xpath (str): XPath of the element.
        element: Web element to search within (optional).

    Returns:
        str:  content of the element.
    """
    try:
        if element:
            return WebDriverWait(element, wait).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        else:
            return WebDriverWait(browser, wait).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
    except:
        return None


def get_element_list(browser, xpath, wait=2, element=None)->List[str]:
    """
    Retrieve text content of an element using XPath.

    Args:
        xpath (str): XPath of the element.
        element: Web element to search within (optional).

    Returns:
        list: Text content of the element.
    """
    try:
        if element:
            return WebDriverWait(element, wait).until(
                EC.presence_of_all_elements_located((By.XPATH, xpath))
            )
        else:
            return WebDriverWait(browser, wait).until(
                EC.presence_of_all_elements_located((By.XPATH, xpath))
            )
    except:
        return None
