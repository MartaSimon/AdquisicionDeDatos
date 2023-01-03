import requests
import argparse
import time
import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def validar_fecha(fecha):
    '''
    Funcion para validar la fecha que se recibe como argumento de entrada
    
    Params
    --------
    fecha: int
    Numero con la fecha recibida como argumento

    Return
    --------
    Lanza una excepcion en caso de que la fecha no tenga el formato correcto, 
    en caso contrario devuelve la fecha
    '''
    if len(fecha) != 8 or not fecha.isdigit():
        raise argparse.ArgumentTypeError("La fecha debe estar en el siguente formato YYYYMMDD. Donde YYYY es el anio, MM es el mes y DD el día.")
    return fecha

def search_and_click(xpath):
    element = driver.find_element(
        By.XPATH, xpath
    )
    element.click()
    time.sleep(1)

url = "https://www.boe.es/diario_borme/"

# En primer lugar, permitimos pasar argumentos al iniciar el programa.
# Con esta librería ya estamos realizando el control de errores, puesto que el argumento fecha es obligatorio.
parser = argparse.ArgumentParser()
parser.add_argument("fecha", type=validar_fecha, help="Fecha del boletín que se quiere descargar")

# Parseamos los argumentos de entrada
fecha = parser.parse_args().fecha
anio = fecha[:4]
mes = fecha[4:6]
dia = fecha[6:]
print(f"Se procede a analizar el boletín del día: {anio}-{mes}-{dia}")

#Tratamos de hacer una peticion a la api en el día seleccionado con requests 
url_borme = "https://www.boe.es/borme/dias/{}/{}/{}".format(anio, mes, dia)
response = requests.get(url_borme)

#Si la respues es un exito (codigo 200), es que hay datos para esa fecha. Sino, no los hay paramos el código
if response.status_code==200:
    print("Datos disponibles en el boletín.")
    # Abrimos selenium para descargar la informacion
    # Indicamos la ruta del driver que debe usar Selenium
    driver_path = "../chromedriver.exe"
    s = Service(driver_path)

    # Establecemos el nombre del directorio en el que queremos almacenar los pdfs descargados
    dir_base= r"C:\Users\marti\Desktop\Boletin_" + fecha
    chromeOptions = webdriver.chrome.options.Options()
    prefs = {'download.default_directory': dir_base, # indicamos el directorio en el que lo queremos descargar
            "plugins.always_open_pdf_externally": True} # Para descargar directamente el pdf, en lugar de abrirlo en el navegador
    chromeOptions.add_experimental_option("prefs",prefs)

    # Antes de inicializar el driver, obtenemos las distintas secciones y el numero de pdfs que hay en cada una, para almacenar cada pdf en su subdirectorio correspondiente
    soup = BeautifulSoup(response.content, "html.parser")
    seccion_segunda = soup.find("div", class_="sumario")#, class_="sumario")

    cabeceras_raw = seccion_segunda.find_all("h4")
    cabeceras = []
    for cabecera in cabeceras_raw:
        cabeceras.append(cabecera.getText())    
    # print(cabeceras) 
    
    longitud = []
    ul_tags = cabeceras_raw[2].find_next_siblings("ul")
    for ul_tag in ul_tags:
        li_tag = ul_tag.findChildren('li', class_="puntoPDF")
        # La longitud de li_tag nos indica cuantos pdfs hay en cada subseccion.
        longitud.append(len(li_tag))
        # print(seccion_segunda)
    # creamos un diccionario con las secciones como claves, y el numero de pdfs por seccion como valores
    subsecciones = dict(zip(cabeceras[2:], longitud))
    print(subsecciones)

    # Inicializamos el driver con la configuracion establecida
    driver = webdriver.Chrome(service=s, options=chromeOptions)
    
    # Accedemos a la url qde la que queremos descargar los datos
    driver.get(url_borme)
    time.sleep(1)
    logging.info('Driver up & running.')

    # Ahora podemos comenzar a navegar
    # En primer lugar, hacemos clic en el desplegable 
    search_and_click(xpath="//div[@class='dropdown']")
    # A continuación, navegamos hasta la seccion segunda
    search_and_click(xpath="//a[text()='SECCIÓN SEGUNDA. Anuncios y avisos legales']")
    # A continuacion, seleccionamos uno a uno los pdfs para descargarlos
    pdfs_list = driver.find_elements(By.XPATH, "//li[@class='puntoPDF']")
    for i, pdf in enumerate(pdfs_list):
        # inicializamos el driver con los directorios en los que queremos almacenar la informacion.
        pdf.click()
   

    

    # Obtenemos el nombre de cada una de las subsecciones mediante la librería requests
    

    # A continuacion, generamos un directorio por sección.



        


else:
    print(f"No se disponen de datos en el Boletín para la fecha {anio}-{mes}-{dia}")

'''
