import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from lib.constants import GOOGLE_CONSOLE_URL


def chech_if_logged_in(driver):
    url_curent = driver.current_url
    if GOOGLE_CONSOLE_URL in url_curent:
        print('[+] Logged in successfully')
        return True
    else:
        print('[-] Not logged in')
        return False


def asteapta_logarea(driver):
    while not driver.current_url.startswith(GOOGLE_CONSOLE_URL):
        time.sleep(1)
    print('[+] Logged in successfully')


def introdu_order(order_id, driver):
    try:
        search_form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'mdc-text-field__input'))
        )
        search_form.clear()
        search_form.send_keys(order_id)
        time.sleep(0.3)
        search_form.send_keys(Keys.ENTER)
        time.sleep(1)
    except TimeoutException:
        print('[-] Nu s-a putut găsi elementul de căutare')
        raise Exception('Nu s-a putut găsi elementul de căutare')


def get_order_status(order_id, driver):
    introdu_order(order_id=order_id, driver=driver)
    element_gasit = asteapta_raspuns_optimizat(driver=driver)
    if element_gasit == 'order':
        intrare_tabel = driver.find_element(By.CLASS_NAME, 'particle-table-row')
        status_cell = intrare_tabel.find_element(By.XPATH, ".//ess-cell[@essfield='order_status_column']")
        status = status_cell.find_element(By.XPATH, ".//span[contains(@class, 'main-text')]").text
        return status
        # Procesează informațiile din tabel aici
    elif element_gasit == 'placeholder':
        return 'Inexistentă'
    else:
        raise Exception('A intervenit o eroare la căutarea comenzii. Încearcă din nou.')


def asteapta_raspuns_optimizat(driver):
    # Definește locatoarele pentru elementele pe care dorești să le verifici
    locator_order = (By.CLASS_NAME, "particle-table-row")
    locator_placeholder = (By.CLASS_NAME, "particle-table-placeholder")

    # Setează un timp maxim de așteptare și un interval de polling
    timp_maxim_asteptare = 10
    interval_polling = 0.5  # Secunde
    timp_start = time.time()

    element_gasit = None
    while (time.time() - timp_start) < timp_maxim_asteptare:
        try:
            element_tabel = driver.find_element(*locator_order)
            if element_tabel.is_displayed():
                element_gasit = 'order'
                break
        except NoSuchElementException:
            pass  # Ignoră dacă elementul nu este găsit

        try:
            element_placeholder = driver.find_element(*locator_placeholder)
            if element_placeholder.is_displayed():
                element_gasit = 'placeholder'
                break
        except NoSuchElementException:
            pass  # Ignoră dacă elementul nu este găsit

        time.sleep(interval_polling)

    return element_gasit
