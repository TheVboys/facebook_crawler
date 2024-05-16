import sys
sys.path.append('../')
from src.const import *
import time


def surf_feed(driver):
    driver.get(base_url)
    start_time = time.time()
    while (time.time() - start_time) < 5 * 60:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

