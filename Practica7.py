import requests
from bs4 import BeautifulSoup
import json

###################################################
##      PRÁCTICA 7.A - BEAUTIFULSOUP
###################################################

# Obtenemos los datos
url = "https://en.wikipedia.org/wiki/Comillas_Pontifical_University"
response = requests.get(url)

# Parseamos el HTML
soup = BeautifulSoup(response.content, "html.parser")

# Buscamos el elemento que queremos inspeccionar
target_tables = soup.find_all("table", class_="infobox vcard")

# Comprobamos que el elemento que hemos obtenido es único
print(f"Hemos encontrado {len(target_tables)} tabla llamada infobox vcard\n\n")

# Declaramos una variable con la tabla de la que vamos a extraer los datos
target_table = target_tables[0]


###################################################
##      PRÁCTICA 7.B - BEAUTIFULSOUP
###################################################

# Inicializamos el diccionario en el que vamos a almacenar los datos que nos interesan 
data = {}

# En primer lugar, buscamos las primeras filas de la tabla, al estar en cursiva, debemos filtrar por elemento i (italics)
italics = target_table.find_all("i")
motto = ["motto_latin", "motto_spanish", "motto_english"]
for i in range(len(italics)):
    data[motto[i]] = italics[i].getText()

# Seguimos buscando las filas que nos faltan, esta vez no están en cursiva, por lo que podremos obtener directamente el texto de los td
# Creamos una lista con las keys que nos falta por encontrar
# Lo vamos recorriendo y buscamos en las rows las distintas cabeceras (th),
# A partir de ahí cogemos el contendido de los td y lo insertamos en la key que se corresponda con la cabecera
keys = ["type","established","chancellor", "vice-chancellor", "rector", "students", "location", "campus", "colors", "affiliations", "website"]

# Buscamos todas las filas de la tabla y las recorremos una a una
rows = target_table.find_all("tr")
for item in rows:
    #  Obtenemos el header de la fila, si no es None. Si es none, se pasa a la siguiente fila
    header = item.find("th")
    if header != None:
        header = header.getText()
    else:
        continue

    # Obtenemos el contenido de la fila. No hay ningun caso en el que la cabecera exista y el contenido sea none, 
    # por lo que no hace falta realizar ninguna comprobacion adicional, aunque lo incluimos para proteger el código
    content = item.find("td")
    if(content != None):
        content = content.getText()
    
    # Una vez localizadas la cabecera y el contenido, lo almacenamos en el diccionario final
    for key in keys:
        # Hacemos una comprobacion para almacenar las keys con el nombre que se requiere
        if(key.strip().lower() == header.strip().lower()):
            data[key] = content

# Para la clave 'affiliations', la clave 'logo' y la clave 'seal', deberemos acceder de forma manual
# La primera de ellas contiene un div adicional que nos impide coger su texto como en el resto de filas
# la segunda y la tercera, al ser una url, deberemos acceder a su href dentro de la etiqueta <a>

# Buscamos affiliations. Está en la posicion 8 de la lista, asique hacemos la busqueda con un limit y escogemos el ultimo valor
# Para insertarlo en la posicion correcta utilizamos
data["affiliations"] = target_table.find_all('td', limit=8)[-1].get_text()

# Buscamos el href del logo. Está en la última posicion de la lista, asique hacemos la busqueda sin limit y escogemos el ultimo valor
data["logo"] = "https://en.wikipedia.org" + target_table.find_all("a")[-1]["href"]

# Buscamos el href del primer logo (seal). Está en la primera posicion de la lista, asique hacemos la busqueda sin limit y escogemos el primer valor
# Lo insertamos al inicio del diccionario, para que conserve el orden deseado
data = {"seal":  "https://en.wikipedia.org" + target_table.find_all("a")[0]["href"], **data}

# Imprimimos el diccionario para ver el resultadoç
print("data = {")
for clave, valor in data.items():
    print(f"'{clave}': '{valor}'")
print("}")

###################################################
##      PRÁCTICA 7.C - JSON
###################################################
# Almacenamos el diccionario creado en un fichero 
with open('../data_comillas.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)