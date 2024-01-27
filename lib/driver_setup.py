from threading import Lock

import undetected_chromedriver as uc

driver = None
lock = Lock()


def init_driver():
    global driver
    if driver is None:
        driver = uc.Chrome()


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
