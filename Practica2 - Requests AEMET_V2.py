from os import stat
import requests
import json
import os
import time


url_base = "https://opendata.aemet.es/opendata/"
endpoint_inventarios = "api/valores/climatologicos/inventarioestaciones/todasestaciones"

api_key = os.environ["AEMET_API_KEY"]

def make_request(url):
    print("Haciendo llamada al endpoint... ", url)
    params = {"api_key": api_key}
    try:
        response = requests.get(url, params=params)
        # S nos devuelve un error de too many requests, esperamos un minuto y lo intentamos de nuevo
        if (response.status_code == 429):
            time.sleep(60)
            response = requests.get(url, params = params)
    except requests.exceptions.RequestException as e:
        print(e)
        raise SystemExit(e)

    return response.status_code, response.json()


def get_climatologias_diarias(fechaIniStr, fechaFinStr, id):
    # Sustituimos los datos en la URL
    url_climatologias="api/valores/climatologicos/diarios/datos/fechaini/{}/fechafin/{}/estacion/{}".format(fechaIniStr,fechaFinStr,id)

    code_2, response = make_request(url_base + url_climatologias)
   
    if(code_2 == 200):
        url_datos = response["datos"]
        code_3, response_final = make_request(url_datos)
        return code_3, response_final



def main():
    # Obtenemos la url para sacar los inventarios
    url_inventario = url_base + endpoint_inventarios
    code_0, inventarios = make_request(url_inventario)
    
    # Si todo ha ido bien, buscamos la estación hacemos una petición para obtener todos
    if(code_0 != 200):
        print("Ha habido un error en la petición... ", code_0)
        return

    #convert string to  object
    inventarios_url = inventarios['datos']
    print("La url obtenida es: " + inventarios_url)
    
    # Hacemos una petición a la url que hemos obtenido con la request anterior
    code_1, all_stations = make_request(inventarios_url)
    # stations_dict = {}
    
    # Si todo ha ido bien, buscamos la estación "MADRID, CIUDAD UNIVERSITARIA"
    if(code_1 != 200):
        print("Ha habido un error en la petición... ", code_1)
        return

    for station in all_stations:
        # Creamos un diccionario con {nombre:id} para cada una de las estaciones para el ejercicio opcional
        # stations_dict[station['nombre']] = station["indicativo"]
        if (station['nombre'] == "MADRID, CIUDAD UNIVERSITARIA"):
            indicativo = station["indicativo"]
            print("Obtenido el indicativo para la estación: ", station["nombre"], "---->", indicativo)
            # Ahora podemos obtener la información de la estación en concreto
            fechaIniStr = "2019-10-01T00:00:00UTC"
            fechaFinStr = "2019-10-30T23:59:59UTC"
            code, response_final = get_climatologias_diarias(fechaIniStr, fechaFinStr, indicativo)
            if(code == 200):
                print(" La respuesta de las climatologías diarias para la estación de 'Madrid, Ciudad universitaria' es: ", response_final)
        # Mostramos el diccionario obtenido
    
    print(len(all_stations))
    #################################
    #       EJERCICIO OPCIONAL      #
    #################################
    # Generamos un diccionario para ir almacenando los datos
    datos_anio_estaciones = {}
    # Hacemos un bucle para recorrer todos los años de los que queremos recopilar informacion
    for year in range(2011, 2021):
        datos_anio_estaciones[year] = {}
        for i in range(len(all_stations)):
            # anio ini y anio fin serán el year analizado en cada iteracion
            endpoint_estacion_mensual = "api/valores/climatologicos/mensualesanuales/datos/anioini/{}/aniofin/{}/estacion/{}".format(year, year, all_stations[i]["indicativo"])
            # print(endpoint_estacion_mensual)
            code_4, response_estacion_mensual = make_request(url_base + endpoint_estacion_mensual)
            if(code_4 != 200):
                print("Ha habido un error en la petición... ", code_4)
                return
            # Para acceder a los datos, debemos hacer una peticion a la url localizada en 'datos' de la respuesta obtenida
            try:
                code_5, response_datos_estacion_mensual = make_request(response_estacion_mensual['datos'])
                if(code_5 != 200):
                    print("Ha habido un error en la petición... ", code_5)
                    return
            except:
                # Si no se encuentra la clave datos para un determinado identificador, se sigue con la siguiente estacion
                continue
                
            # De esta respuesta, queremos obtener el campo 'tm_mes', que equivale a la temperatura media, unicamente de los meses de agosto
            for data_month in response_datos_estacion_mensual:
                # Nos interesan solamente los meses de agosto
                if(data_month['fecha'] == str(year) + '-8'):
                    try:
                        datos_anio_estaciones[year][data_month['indicativo']] = data_month['tm_mes']
                    except:
                        continue

    print(datos_anio_estaciones)
    # Hemos conseguido un diccionario del tipo:
    # {año: {id_estacion: t_media_agosto}}

    # Para generar un array que contenga la temp media nacional por año, recorremos el diccionario
    array_final = []
    # vamos a generar también un diccionario para que sea más explicativo
    dict_final = {}
    for year, estaciones in datos_anio_estaciones.items():
        print("Calculando la media para el año ", year)
        suma = 0
        for i in estaciones:
            suma += float(estaciones[i]) 
        array_final.append(suma/len(estaciones))
        dict_final[year] = suma/len(estaciones)

    print("La media de temperaturas en el mes de agosto por año es: ", array_final)
    print("La media de temperaturas en el mes de agosto por año es: ",dict_final)


if __name__ == "__main__":
    main()