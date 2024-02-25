import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from lib.constants import GOOGLE_CONSOLE_URL, TIMP_ASTEPTARE, TIMP_ASTEPTARE_DELAY_UI, TIMP_ASTEPTARE_DELAY_UI_MARE, \
    INTERVAL_POLLING


def chech_if_logged_in(driver):
    url_curent = driver.current_url
    if GOOGLE_CONSOLE_URL in url_curent:
        return True
    else:
        return False


def asteapta_logarea(driver):
    for i in range(0, TIMP_ASTEPTARE):
        if driver.current_url.startswith(GOOGLE_CONSOLE_URL):
            return
        else:
            time.sleep(1)
    raise Exception('Nu s-a putut face logarea')


def introdu_order(order_id, driver):
    try:
        search_form = WebDriverWait(driver, TIMP_ASTEPTARE).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'mdc-text-field__input'))
        )
        search_form.clear()
        time.sleep(TIMP_ASTEPTARE_DELAY_UI)
        search_form.send_keys(order_id)
        time.sleep(TIMP_ASTEPTARE_DELAY_UI)
        search_form.send_keys(Keys.ENTER)
        time.sleep(TIMP_ASTEPTARE_DELAY_UI_MARE)
    except TimeoutException:
        print('[-] Nu s-a putut găsi elementul de căutare')
        raise Exception('Nu s-a putut găsi elementul de căutare')


def get_order_status(order_id, driver, inexistent=False):
    introdu_order(order_id=order_id, driver=driver)
    element_gasit = asteapta_raspuns_optimizat(driver=driver, order_id=order_id)
    if element_gasit == 'order':
        intrare_tabel = driver.find_element(By.CLASS_NAME, 'particle-table-row')
        status_cell = intrare_tabel.find_element(By.XPATH, ".//ess-cell[@essfield='order_status_column']")
        status = status_cell.find_element(By.XPATH, ".//span[contains(@class, 'main-text')]").text
        return status
        # Procesează informațiile din tabel aici
    elif element_gasit == 'placeholder':
        if inexistent:
            return 'Inexistentă'
        else:
            print('[-] Comanda nu a fost găsită se reincearca in 10 secunde')
            time.sleep(10)
            return get_order_status(order_id=order_id, driver=driver, inexistent=True)
    else:
        raise Exception('A intervenit o eroare la căutarea comenzii. Încearcă din nou.')


def asteapta_raspuns_optimizat(driver, order_id):
    # Definește locatoarele pentru elementele pe care dorești să le verifici
    locator_order = (By.CLASS_NAME, "particle-table-row")
    locator_placeholder = (By.CLASS_NAME, "particle-table-placeholder")

    # Setează un timp maxim de așteptare și un interval de polling

    timp_start = time.time()

    element_gasit = None
    while (time.time() - timp_start) < TIMP_ASTEPTARE:
        try:
            element_tabel = driver.find_elements(*locator_order)
            if len(element_tabel) > 1:
                print('[-] Mai multe elemente găsite')
                pass
            elif len(element_tabel) == 1:
                if element_tabel[0].is_displayed():
                    id_comanda = element_tabel[0].find_element(By.XPATH, ".//ess-cell[@essfield='order_id_column']").text
                    if id_comanda == order_id:
                        element_gasit = 'order'
                        break
                    else:
                        print('[-] Comanda găsită nu corespunde cu cea căutată')
        except NoSuchElementException:
            pass  # Ignoră dacă elementul nu este găsit

        try:
            element_placeholder = driver.find_element(*locator_placeholder)
            if element_placeholder.is_displayed():
                element_gasit = 'placeholder'
                break
        except NoSuchElementException:
            pass  # Ignoră dacă elementul nu este găsit

        time.sleep(INTERVAL_POLLING)

    return element_gasit
