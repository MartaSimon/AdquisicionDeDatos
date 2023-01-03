import requests
from bs4 import BeautifulSoup
import json

#################################################
#   PARTE1: BÚSQUEDA DE LA TABLA
#################################################
# Obtenemos los datos
url = "https://en.wikipedia.org/wiki/World_population"
response = requests.get(url)

# Parseamos el HTML
soup = BeautifulSoup(response.content, "html.parser")

# Buscamos el elemento que queremos inspeccionar
target_tables = soup.find_all("table", {'class':["wikitable", "sortable", "jquery-tablesorter"]})

# Comprobamos que el elemento que hemos obtenido es único
print(f"Hemos encontrado {len(target_tables)} tabla llamada wikitable sortable jquery-tablesorter\n\n")

# Declaramos una variable con la tabla de la que vamos a extraer los datos. En nuestro caso, es la que se encuentra en la tercera posicion
target_table = target_tables[2]

#################################################
#   PARTE2: OBTENCION DE LOS DATOS
#################################################
# Inicializamos el diccionario en el que vamos a almacenar los datos que nos interesan 
data = {}

# Buscamos todas las filas de la tabla y las recorremos una a una
rows = target_table.find_all("tr")
headers = []
for i, item in enumerate(rows):
    # En la primera fila encontramos las cabeceras, vamos a almacenarlas en una lista para insertarlas después una a una en el diccionario por cada continente
    if i == 0:
        headers_raw = item.find_all("th")
        for header in headers_raw:
            # Los argumentos pasados al método getText sirven para obtener todos los tipos de texto que contiene la cabecera, unirlos con un espacio
            headers.append(header.getText(" ", strip=True))
        # print("Headers: ", headers)
    # En el resto de filas, analizamos la informacion de cada uno de los continentes
    else:
        info_raw = item.find_all("td")
        # Recorremos celda a celda cada una de las filas de cada continente. Lo hacemos con un enumerate para saber por qué celda vamos
        for z, info in enumerate(info_raw):
            
            # En la primera columna, inicializamos el diccionario que contendrá los datos del continente
            if z==0: 
                country = info.getText(strip=True)
                data[country]={}
            print("####",country)
            print(info)
            # A partir de la segunda columna
            if z!=0:
                # Buscamos si existe algun link en la celda que estamos inspeccionando, para añadirlo a la entrada del diccionario
                if info.find("a"):
                    data[country][headers[z]] = {}
                    data[country][headers[z]]["Text"] = info.getText(strip=True)
                    data[country][headers[z]]["Link"] = "https://en.wikipedia.org" + info.a["href"]
                # Buscamos si existe alguna imagen en la celda que estamos inspeccionando, para añadirla a la entrada del diccionario
                if info.find("img"):
                    data[country][headers[z]]["Image"] = "https://en.wikipedia.org" + info.img["src"]
                # Si la celda no contiene ni links ni imagenes, insertamos el texto en la clave del diccionario correspondiente
                else:
                    data[country][headers[z]] = info.getText(strip=True)
            print("--------------------------------------------------------------------")

print(f"El diccionario final es: {data}")



#################################################
#   PARTE3: ALMACENAMIENTO DE LOS DATOS EN JSON
#################################################
# Almacenamos el diccionario creado en un fichero 
path = '../data_continentes.json'
with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print(f"Diccionario almacenado en el fichero {path}")