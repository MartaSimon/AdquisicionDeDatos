import requests
from bs4 import BeautifulSoup
import csv

#########################################################
#   PRIMER NIVEL: Obtener las URLs de los países        #
#########################################################
def make_request(url):
    '''
    Realiza una llamada con la librería request de python a la url que recibe como argumento.
    Devuelve el HTML de la págima parseado por la librería bs4 de python.
    
    Params
    -------
    url : str
    La url completa a la que hacer la llamada.
    
    Return
    -------
    soup: HTML de la página parseado por Beautifulsoup
    '''
    response = requests.get(url)
    # Parseamos el HTML
    soup = BeautifulSoup(response.content, "html.parser")
    # Devolvemos el HTML parseado
    return soup

def save_response(path, data):
    '''
    Almacena en un fichero csv, cuyo nombre recibe como argumento, una lista recibida también por argumento.
    
    Params
    -------
    path : str
    El path absoluto del fichero en el que se quieren almacenar los datos.
    
    data: list
    La lista que se quiere persistir en el fichero
    '''
    with open(path, "w",newline='') as output_file:
        writer = csv.writer(output_file , delimiter =";")
        for row in data:
            if not row: continue # Para windows
            writer.writerow(row)


# Definimos la url a la que vamos a hacer la peticion
url = "https://en.wikipedia.org/wiki/Lists_of_universities_and_colleges_by_country"
# Hacemos una llamada al método make_request con la url anterior
soup = make_request(url)

# Buscamos todos los elementos de las listas de la página
ul_list = soup.find_all("ul")

countries = []
# Recorremos desde el elemento 3 hasta el 12, que son los que nos interesan (continentes)
for item in ul_list[3:12]:
    # Buscamos todos los elementos de la lista para cada continente y los recorremos para obtener sus hrefs
    continent  = item.find_all("li")
    for country in continent:
        # Evitamos United Kingdom puesto que tiene un formato diferente
        if not 'United Kingdom' in country.get_text():
            countries.append([country.get_text(), country.a['href']])
            

# Eliminamos duplicados 
for element in countries:
    if countries.count(element) > 1:
        countries.remove(element)
print("Continentes encontrados: ", countries)
# Almacenamos la lista creada en un fichero 
path_countries = "../countries.csv"
save_response(path_countries, countries)
        

#################################################################
#   SEGUNDO NIVEL: Obtener las URLs de las universidades        #
#################################################################
# Abrimos el fichero que acabamos de almacenar, y lo guardamos en una variable llamada country_matrix
with open(path_countries, "r") as input_file:
    reader = csv.reader(input_file , delimiter =";")
    country_matrix = [row for row in reader] 

for country in country_matrix:
    # Vamos a obtener solamente las urls de Alemania
    if(country[0] == "Germany"):
        url_aux = country[1]
        # Añadimos la url base de wikipedia para poder realizar la peticion a una url bien formada
        url = "https://en.wikipedia.org" + url_aux
        # Hacemos una llamada al método make_request con la url obtenida
        soup = make_request(url)
        
        # Buscamos dentro del html de la pagina la tabla que necesitamos
        table_germany = soup.find("table", class_="wikitable sortable")

        # Inicializamos una lista para ir almacenando las universidades
        saved_universities = []
        # Vamos recorriendo las universidades de la tabla
        for item in table_germany:
            # Para cada fila, obtenemos el texto y su correspondiente enlace
            universities_row  = table_germany.find_all("tr")
            for university in universities_row[1:]:
                univ_col = university.find_all("td")[0]
                saved_universities.append([country[0],url,univ_col.get_text().replace("\n", ""), univ_col.a['href']])

print("Universidades de Alemania: ", saved_universities)
# Almacenamos la lista creada en un fichero 
path_university = "../universities.csv"
save_response(path_university, saved_universities)
