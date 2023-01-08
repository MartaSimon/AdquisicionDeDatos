import requests
import os
import time


url_base = "https://opendata.aemet.es/opendata/"
endpoint_inventarios = "api/valores/climatologicos/inventarioestaciones/todasestaciones"

'''
                    ¡IMPORTANTE! 

Para que la siguiente linea funcione, es necesario tener una variable de entorno llamada AEMET_API_KEY con el API_KEY personal asignado por la AEMET.

Para setear la variable de entorno debemos ejecutar desde una terminal el siguiente código:
    > set AEMET_API_KEY=tu_api_key_personal

Para comprobar que la variable de entorno se ha configurado correctamente, desde la misma terminal ejecutamos el siguiente código:
    > echo %AEMET_API_KEY%
''' 
api_key = os.environ["AEMET_API_KEY"]

def make_request(url):
    '''
    Realiza una llamada con la librería request de python a la url que recibe como argumento.
    Devuelve el código de respuesta de la api y el contenido de la misma.
    
    Params
    -------
    url : str
    La url completa a la que hacer la llamada.
    
    Return
    -------
    status_code : int
    Código de respuesta de la api
    
    response.json: dict
    Diccionario con la respuesta de la api en formato json.
    '''
    print("Haciendo llamada al endpoint... ", url)
    params = {"api_key": api_key}
    try:
        response = requests.get(url, params=params)
        # Si nos devuelve un error de too many requests(429), esperamos un minuto y lo intentamos de nuevo
        if (response.status_code == 429):
            time.sleep(60)
            response = requests.get(url, params = params)
    except requests.exceptions.RequestException as e:
        print(e)
        raise SystemExit(e)

    return response.status_code, response.json()


def get_climatologias_diarias(fechaIniStr, fechaFinStr, id):
    '''
    Obtiene las climatologías de los dias comprendidos entre las fechas de inicio y final que recibe como argumento
    para la estacion correspondiente al id que también recibe como argumento.
    
    Params
    -------
    fechaIniStr : str
    La fecha de inicio de los dias de los que queremos obtener la climatología.

    fechaFinStr: str
    La fecha de fin de los dias de los que queremos obtener la climatología.
    
    id:
    El identificador de la estacion de la que queremos conocer los datos.

    Return
    -------
    status_code : int
    Código de respuesta de la api
    
    response.json: dict
    Diccionario con la respuesta de la api en formato json.

    '''
    # Sustituimos los datos en la URL
    url_climatologias="api/valores/climatologicos/diarios/datos/fechaini/{}/fechafin/{}/estacion/{}".format(fechaIniStr,fechaFinStr,id)

    code_2, response = make_request(url_base + url_climatologias)
   
    # Si obtenemos una respuesta satisfactoria de la api, podemos realizar la busqueda de la estacion correspondiente en los días indicados
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

    # Obtenemos la url recibida como respuesta de la peticion anterior
    inventarios_url = inventarios['datos']
    print("La url obtenida es: " + inventarios_url)
    
    # Hacemos una petición a la url que hemos obtenido con la request anterior
    code_1, all_stations = make_request(inventarios_url)
    
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
            # Mostramos el diccionario obtenido
            if(code == 200):
                print(" La respuesta de las climatologías diarias para la estación de 'Madrid, Ciudad universitaria' es: ", response_final)
        
    
    print(len(all_stations))
    
    #################################
    #       EJERCICIO OPCIONAL      #
    #################################
    # Comenzamos con un sleep para que podamos ver las salidas del ejercicio anterior
    time.sleep(5)
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
    print("La media de temperaturas en el mes de agosto por año es: ", dict_final)


if __name__ == "__main__":
    main()