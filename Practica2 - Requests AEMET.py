from os import stat
import requests
import json


url_base = "https://opendata.aemet.es/opendata/"
token_profe = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqYWRyYXF1ZUBoZXkuY29tIiwianRpIjoiZmM1ODIwZTMtZWMwYS00MGU4LTgxZDAtNTQ5NTU2ZGE2MDRiIiwiaXNzIjoiQUVNRVQiLCJpYXQiOjE2MDQwNjM0OTMsInVzZXJJZCI6ImZjNTgyMGUzLWVjMGEtNDBlOC04MWQwLTU0OTU1NmRhNjA0YiIsInJvbGUiOiIifQ.X0Xis-NkWZ2ljH6DeYePgcvwS4imU1u9Bo2wy1zeZH4"

def get_inventario():
    endpoint_inventario= "api/valores/climatologicos/inventarioestaciones/todasestaciones"
    print("Obteniendo inventarios...", url_base+endpoint_inventario)
    params = {"api_key": token_profe}
    response = requests.get(url_base + endpoint_inventario, params=params)

    return response.status_code, response.json()

def get_specific_station(url):
    params = {"api_key": token_profe}
    response = requests.get(url, params=params)
    
    return response.status_code, response.json()

def get_climatologias_diarias(id):
    fechaIniStr = "2019-10-01T00:00:00UTC"
    fechaFinStr = "2019-10-30T23:59:59UTC"
    idema = id

    url_climatologias="/api/valores/climatologicos/diarios/datos/fechaini/{}/fechafin/{}/estacion/{}".format(fechaIniStr,fechaFinStr,idema)
    print(url_climatologias)

    params = {"api_key": token_profe}
    response = requests.get(url_base+url_climatologias, params=params)
    url_datos = response.json()["datos"]
    print("La URL de donde buscar los datos de la estación 'MADRID, CIUDAD UNIVERSITARIA' es: ", url_datos)

    response_final = requests.get(url_datos, params=params)
    #print("Los datos obtenidos son: ", response_final.json())
    return response_final




def main():
    # Obtenemos la url para sacar los inventarios
    code_0, inventarios = get_inventario()
    # Si todo ha ido bien, buscamos la estación hacemos una petición para obtener todos
    if(code_0 == 200):
        #convert string to  object
        inventarios_url = inventarios['datos']
        print("La url obtenida es: " + inventarios_url)
        # Hacemos una petición a la url que hemos obtenido con la request anterior
        code_1, all_stations = get_specific_station(inventarios_url)
        # SI todo ha ido bien, buscamos la estación "MADRID, CIUDAD UNIVERSITARIA"
        if(code_1 == 200):
            for station in all_stations:
                if (station['nombre'] == "MADRID, CIUDAD UNIVERSITARIA"):
                    indicativo = station["indicativo"]
                    print("Obtenido el indicativo para la estación: ", station["nombre"], "---->", indicativo)
                    # Ahora podemos obtener la información de la estación en concreto
                    get_climatologias_diarias(indicativo)



if __name__ == "__main__":
    main()