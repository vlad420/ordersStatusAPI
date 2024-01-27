from threading import Lock

import undetected_chromedriver as uc


from lib.utils import get_chrome_profile_path

driver = None
lock = Lock()


def init_driver(headless=False):
    global driver
    if driver is None:
        driver = uc.Chrome(headless=headless, user_data_dir=get_chrome_profile_path())


def get_driver():
    global driver
    if driver is None:
        init_driver()
    return driver


def get_lock():
    global lock
    return lock


def shutdown_driver():
    global driver
    if driver:
        driver.quit()
