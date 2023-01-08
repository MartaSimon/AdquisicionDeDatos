import time
import logging
import sys

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

'''
    La página web sobre la que se realiza esta práctica está en mantenimiento
    esta entrega contiene sólamente la parte de la práctica que me dio tiempo 
    a hacer el día de clase.
'''

def find_click_element(driver, xpath):
    '''
    Función para seleccionar y hacer click en un elemento concreto de la página

    Params
    --------
    driver: driver
    El driver de selenium necesario para buscar el elemento y hacer el click

    xpath: string
    Ruta del HTML del elemento que se quiere buscar y hacer click sobre él       
    '''
    element = driver.find_element(
        By.XPATH, xpath
    )
    element.click()
    time.sleep(1)

    return element

def find_elements(driver, xpath):
    '''
    Función para seleccionar varios elementos con el mismo xpath de la página
    
    Params
    --------
    driver: driver
    El driver de selenium necesario para buscar el elemento

    xpath: string
    Ruta del HTML de los elementos que se quieren buscar

    Return
    ------
    elements: list
    Una lista con uno o varios elementos, en funcion del numero de elementos 
    que haya en la pagina con el xpath indicado     
    '''
    elements = driver.find_elements(
        By.XPATH, xpath
    )
    return elements

# Indicamos donde se encuentra el driver e inicializamos el servicio y el driver
driver_path = "../chromedriver.exe"
s = Service(driver_path)
driver = webdriver.Chrome(service=s)

# Definimos la url sobre la que vamos a navegar y se la indicamos al driver
url = 'https://comparador.cnmc.gob.es/'
driver.get(url)
time.sleep(1)
logging.info('Driver up & running.')

# Localizamos el boton de denegar y clicamos sobre el
find_click_element(driver, "//button[@class='cookiesjsr-btn']")

# Localizamos el formulario y lo desplegamos
find_click_element(driver, "//div[@class='v-input__append-inner']")

# Realizmos una búsqueda de todos los elementos de la lista del dropdown
dropdown_suministro = find_elements(driver, "//div[@class='v-list-item__title']")

# Buscamos el elemento electricidad y hacemos click sobre él
for tipo in dropdown_suministro:
    try:
        if tipo.text == "Electricidad":
            tipo.click()
            time.sleep(1)
    except:pass

# Localizamos el boton de iniciar y clicamos sobre el
find_click_element(driver, "//button[contains(@class, 'v-btn v-btn--is-elevated')]")

# Ahora rellenamos el formulario, el campo que nos piden
postal_code = 28008

# Localizamos el input del codigo postal e introducimos el valor definido
input_postalcode = driver.find_element(
    By.XPATH, "//input[@name='codigoPostal']"
)
input_postalcode.send_keys(postal_code)
time.sleep(1)

# Localizamos el boton de continuar y clicamos sobre el
find_click_element(driver, "//button[contains(@class, 'v-btn v-btn--is-elevated v-btn--has-bg theme--light v-size--default secondary')]")

# Una vez mas, buscamos el checkbox para confirmar que hemos leido los terminos y condiciones y continuamos
find_click_element(driver, "//div[@class='v-input--selection-controls__ripple']")

# Localizamos el boton de continuar y clicamos sobre el. Al ser una ventana flotante, existen muchos botones con la misma clase, 
# puesto que también lee los botones que hay debajo. Buscamos todos y después hacemos click en el de continuar
buttons = find_elements(driver, "//button[contains(@class, 'v-btn v-btn--is-elevated v-btn--has-bg theme--light v-size--default secondary')]")

for button in buttons:
    try:
        if button.text == "Continuar":
            button.click()
            time.sleep(1)
    except:pass


# TODO: Buscar primero por filas, luego por columnas
# en el caso concreto de la col 1 coger la imagen








