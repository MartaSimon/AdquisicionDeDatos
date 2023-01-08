import requests
import argparse
import time
import logging
import os, os.path


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
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
    '''
    Función para seleccionar y hacer click en un elemento concreto de la página

    Params
    --------
    xpath: string
    Ruta del HTML del elemento que se quiere buscar y hacer click sobre él    
    '''
    element = driver.find_element(
        By.XPATH, xpath
    )
    element.click()
    time.sleep(1)

def safe_open_w(path):
    ''' 
    Abre la ruta que recibe como argumento para escribir un determinado fichero,
    creando todos los directorios necesarios siempre y cuando no existan.

    Params
    --------
    path: string
    Ruta en la que se quiere escribir los ficheros

    Return
    --------
    output_file: file
    Fichero en el que se va a escribir abierto en formato binario (para soportar pdfs)
    '''

    os.makedirs(os.path.dirname(path), exist_ok=True)
    output_file = open(path, 'wb')
    return output_file

#############################
#       FASE DE SPIDER      #      
#############################

# Url a la que se va a realizar la primera llamada
url = "https://www.boe.es/diario_borme/"

# En primer lugar, permitimos pasar argumentos al iniciar el programa.
# Con esta librería ya estamos realizando el control de errores, puesto que el argumento fecha es obligatorio.
# Además, indicando la funcion validar_fecha en el argumento tipo, estamos ejecutando la funcion con dicho nombre 
# para que valide el formato del argumento de entrada
parser = argparse.ArgumentParser()
parser.add_argument("fecha", type=validar_fecha, help="Fecha del boletín que se quiere descargar")

# Parseamos los argumentos de entrada
fecha = parser.parse_args().fecha
anio = fecha[:4]
mes = fecha[4:6]
dia = fecha[6:]
print(f"Se procede a analizar el boletín del día: {anio}-{mes}-{dia}")

#Tratamos de hacer una peticion a la api en el día seleccionado con requests, para comprobar que existe 
url_borme = "https://www.boe.es/borme/dias/{}/{}/{}".format(anio, mes, dia)
response = requests.get(url_borme)

#Si la respues es un exito (codigo 200), es que hay datos para esa fecha. Sino, no los hay paramos el código
if response.status_code==200:
    print("Datos disponibles en el boletín.")
    # Abrimos selenium para navegar hasta la página y seccion deseadas
    # Indicamos la ruta del driver que debe usar Selenium
    driver_path = "../chromedriver.exe"
    s = Service(driver_path)  

    # Inicializamos el driver con la configuracion establecida
    driver = webdriver.Chrome(service=s)
    
    # Accedemos a la url qde la que queremos descargar los datos
    driver.get(url_borme)
    time.sleep(1)
    logging.info('Driver up & running.')

    # Ahora podemos comenzar a navegar
    # En primer lugar, hacemos clic en el desplegable 
    search_and_click(xpath="//div[@class='dropdown']")

    # A continuación, navegamos hasta la seccion segunda
    search_and_click(xpath="//a[text()='SECCIÓN SEGUNDA. Anuncios y avisos legales']")

    # Obtenemos la url de dicha seccion
    url_seccion_segunda = driver.current_url
    print("URL de la pagina actual:", driver.current_url)

    # Una vez hemos navegado hasta la página que queremos, podemos cerrar el driver. El trabajo de descarga lo haremos mediante la librería requests
    '''
    # Comentado ya que tarda en ejecutarse, y el driver se cierra al final de la ejecución del código automáticamente
    driver.close()
    print("Cerrando el driver")
    '''

    ###############################
    #       FASE DE SCRAPPER      #      
    ###############################

    # Una vez obtenida la seccion actual, realizamos un request a dicha url para obtener su html, parsearlo y poder descargar los pdfs
    response = requests.get(url_seccion_segunda)
    soup = BeautifulSoup(response.content, "html.parser")

    # Buscamos el div que contiene toda la informacion que necesitamos
    seccion_segunda = soup.find("div", class_="sumario")
    # Obtenemos cada una de las subsecciones de la seccion segunda
    cabeceras_raw = seccion_segunda.find_all("h4")

    # Almacenamos todas las cabeceras para, posteriormente, crear los subdirectorios y almacenar los pdfs
    cabeceras = []
    for cabecera in cabeceras_raw:
        cabeceras.append(cabecera.getText())
    
    # Establecemos el nombre del directorio en el que queremos almacenar los pdfs descargados
    # Está compuesta por el nombre boletín seguido de la fecha del mismo
    dir_base= "../BROME/Boletin_" + fecha 
    
    # Vamos descargando cada uno de los pdfs de cada subseccion en su directorio correspondiente.
    ul_tags = cabeceras_raw[0].find_next_siblings("ul")
    for i, ul_tag in enumerate(ul_tags):
        # Obtenemos el nombre de la seccion actual
        seccion_actual = cabeceras[i]

        # Obtenemos todos los pdfs de dicha seccion, es decir, los children de tipo li de cada h4
        li_tag = ul_tag.findChildren('li', class_="puntoPDF")
        
        # Recorremos cada uno de los li (pdfs) de cada seccion
        for pdf in li_tag:            
            # Obtenemos la url del pdf para poder descagrarlo
            url_pdf = "https://www.boe.es/" + pdf.a["href"]
           
            # Accedemos al nombre del pdf para guardarlo correctamente
            nombre_pdf = url_pdf.split("/")[-1]
            
            # Generamos la ruta para cada pdf, que está compuesta por: 
            #   - El nombre y la fecha del boletín 
            #   - Un número (i), para que se muestren en el mismo orden que en la web cada una de las secciones en el explorador de archivos
            #   - El nombre de la seccion actual
            #   - El nombre del pdf que se va a almacenar
            ruta_pdf = dir_base+"/"+str(i)+"_"+seccion_actual+"/"+ nombre_pdf

            # Realizamos una request para obtener el contenido del pdf
            response_pdf = requests.get(url_pdf)
            
            # Utilizamos la funcion safe_open_w definida al inicio de este fichero para que se cree el directorio en caso de que no exista
            with safe_open_w(ruta_pdf) as output_file:
                print("Guardando pdf en: " + ruta_pdf)
                output_file.write(response_pdf.content)
        
        ########################################
        #   APARTADO OPCIONAL: DESCARGA XML    #
        ########################################
        # Buscamos la url de descarga de otros formatos
        otros_formatos_tag = ul_tag.findChildren('li', class_="puntoHTML")
        for otros_formatos in otros_formatos_tag:
            # Obtenemos la url de la página de otros formatos para navegar hasta ella y poder descargar el XML
            url_otros_formatos = "https://www.boe.es/" + otros_formatos.a["href"]
            # print(url_otros_formatos)
            # realizamos una peticion para navegar a la página en la que se encuentra el XML
            response_otros_formatos = requests.get(url_otros_formatos)

            # Una vez en dicha página, parseamos el html para obtener el link que nos interesa y poder descargar el XML
            soup_otros_formatos = BeautifulSoup(response_otros_formatos.content, "html.parser")
            xml_link = "https://www.boe.es/" + soup_otros_formatos.find("a", title="Texto y metadatos en formato XML")["href"]

            # Realizamos una última peticion al link del xml para poder descargarlo
            response_xml = requests.get(xml_link)

            # Accedemos al nombre del pdf para guardarlo correctamente
            nombre_xml = xml_link.split("=")[-1]

            # Almacenamos la respuesta en la ruta deseada
            ruta_xml = dir_base+"/"+str(i)+"_"+seccion_actual+"/"+ nombre_xml + ".xml"

            # Utilizamos la funcion safe_open_w definida al inicio de este fichero para que se cree el directorio en caso de que no exista
            with safe_open_w(ruta_xml) as output_file:
                print("Guardando xml en: " + ruta_xml)
                output_file.write(response_xml.content)

else:
    print(f"No se disponen de datos en el Boletín para la fecha {anio}-{mes}-{dia}")
