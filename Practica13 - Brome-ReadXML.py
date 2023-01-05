import argparse
import os

from bs4 import BeautifulSoup


def validar_ruta(xml_file):
    '''
    Funcion que comprueba si la ruta pasada por argumento al programa existe y si el fichero esperado está en formato xml

    Params
    --------
    xml_file: string
    Ruta del fichero que se quiere parsear

    Return
    --------
    Lanza una excepcion en caso de que el fichero no exista o no esté en el formato correcto.
    '''
    if not os.path.exists(xml_file):
        raise argparse.ArgumentTypeError("La ruta indicada no existe")
    # Obtener la extensión del archivo
    _, file_extension = os.path.splitext(xml_file)
    if file_extension != ".xml":
        raise argparse.ArgumentTypeError("Se debe especificar un fichero xml")
    return xml_file

# Declaramos un argumento obligatorio que habrá que pasarle al programa
parser = argparse.ArgumentParser()
parser.add_argument("xml_file", type=validar_ruta, help="Ruta del archivo xml que se quiere parsear")

# Leemos el contenido del fichero que se ha pasado como argumento al programa en la variable xml_content
xml_file = parser.parse_args().xml_file
with open(xml_file) as input_file:
    xml_content = input_file.read()

# Parseamos el contenido del fichero con la librería beautifulsoup
# Si el módulo no está instalado, deberemos instalarlo con el comando:
#   > pip install lxml
soup = BeautifulSoup(xml_content, 'xml')

# Comprobamos que se ha parseado corractamente
print("Imprimiendo contenido del xml: " + soup.prettify())

# Buscamos todas las etiquetas de clase parrafo
parrafos = soup.find_all("p", class_ = 'parrafo')

print("LOS PÁRRAFOS DEL DOCUMENTO XML SON:")
# Print the tag name and attributes of the elements
for parrafo in parrafos:
    print("--> ", parrafo.getText())
