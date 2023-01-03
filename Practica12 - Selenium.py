import time
import logging
import sys

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

driver_path = "../chromedriver.exe"
s = Service(driver_path)
driver = webdriver.Chrome(service=s)

url = 'https://comparador.cnmc.gob.es/'
driver.get(url)
time.sleep(1)
logging.info('Driver up & running.')

# Localizamos el boton de denegar y clicamos sobre el
denegar_button = driver.find_element(
    By.XPATH, "//button[@class='cookiesjsr-btn']"
)
denegar_button.click()
time.sleep(1)

# Localizamos el formulario y lo desplegamos
display_dropdown_suministro = driver.find_element(
    By.XPATH, "//div[@class='v-input__append-inner']"
)
# Hacemos click sobre el dropdown para poder seleccionar el elemento Electricidad de la lista
display_dropdown_suministro.click()
time.sleep(1)


# Localizamos el formulario y lo desplegamos
dropdown_suministro = driver.find_elements(
    By.XPATH, "//div[@class='v-list-item__title']"
)

for tipo in dropdown_suministro:
    try:
        if tipo.text == "Electricidad":
            tipo.click()
            time.sleep(1)
    except:pass

# Localizamos el boton de iniciar y clicamos sobre el
iniciar_button = driver.find_element(
    By.XPATH, "//button[contains(@class, 'v-btn v-btn--is-elevated')]"
)

iniciar_button.click()
time.sleep(1)

# Ahora rellenamos el formulario, el campo que nos piden
postal_code = 28008

# Localizamos el boton de iniciar y clicamos sobre el
input_postalcode = driver.find_element(
    By.XPATH, "//input[@name='codigoPostal']"
)
input_postalcode.send_keys(postal_code)
time.sleep(1)

# Buscamos el botón de continuar y hacemos click sobre el

# Localizamos el boton de iniciar y clicamos sobre el
buscar_button = driver.find_element(
    By.XPATH, "//button[contains(@class, 'v-btn v-btn--is-elevated v-btn--has-bg theme--light v-size--default secondary')]"
)

buscar_button.click()
time.sleep(1)

# Una vez mas, buscamos el elemento para afirmar que hemos leido los terminos y condiciones y continuamos
check_terminos = driver.find_element(
    By.XPATH, "//div[@class='v-input--selection-controls__ripple']"
)
check_terminos.click()
time.sleep(1)

# Localizamos el boton de continuar y clicamos sobre el
buttons = driver.find_element(
    By.XPATH, "//button[contains(@class, 'v-btn v-btn--is-elevated v-btn--has-bg theme--light v-size--default secondary')]"
)

for button in buttons:
    try:
        if button.text == "Electricidad":
            tipo.click()
            time.sleep(1)
    except:pass

continuar_button.click()
time.sleep(2)


# buscar primero por filas, luego por columnas
# en el caso concreto de la col 1 coger la imahen






