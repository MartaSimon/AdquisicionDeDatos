import json
import numpy as np

def load_json(path):
    """
    Loads JSON file in given path into a dictionary that will
    be returned.
    Params
    -------
    path : str
    The path to the target JSON file.
    Return
    -------
    d : dic
    The dictionary with the JSON content loaded.
    """
    with open(path, "r") as input_file:
        d = json.load(input_file)
        return d

# Cargamos las estadísitcas en un json
d = load_json("../kobe.json")

headers_needed = [ "SEASON_ID","PLAYER_AGE","GP","PTS","AST","REB"]
# obtenemos los indices de las cabeceras que nos interesan
header_index = [d["resultSets"]["name" == "SeasonTotalsRegularSeason"]["headers"].index(e) for e in headers_needed]
# print(header_index)

regular_season_stats = []
# Añadimos las cabeceras a la lista
regular_season_stats.append(["AÑO DE LA TEMPORADA", "EDAD DEL JUGADOR", "PARTIDOS DISPUTADOS", "MEDIA DE PUNTOS ANOTADOS", "MEDIA DE ASISTENCIAS REPARTIDAS", "MEDIA DE REBOTES RECOGIDOS"])
    
for item_dict in d["resultSets"]["name" == "SeasonTotalsRegularSeason"]["rowSet"]:
    aux_list = []
    for index in header_index:
        # np_item_list = np.array(item_list)
        aux_list.append(item_dict[index])
    regular_season_stats.append(aux_list)
            
print("La matriz obtenida es la siguiente: \n", regular_season_stats)

# Una vez generada la matriz...
# 1. Obtén la temporada con mayor y menor cantidad total de puntos anotados
#       Para esto tendremos que multiplicar la "MEDIA DE PUNTOS ANOTADOS" por "PARTIDOS DISPUTADOS", y obtener el máximo y minimo valor
# 2. Obtén la media de puntos absoluta durante toda la carrera de Kobe Bryant
#       Para esto, tendremos que que multiplicar por cada temporada la columna "MEDIA DE PUNTOS ANOTADOS" por "PARTIDOS DISPUTADOS"
#       y dividir por el total de partidos disputados a lo largo de la carrera.
# 3. obtener también la media absoluta de rebotes y asistencias 
#       Para esto, tendremos que realizar la misma operacion que en el apartado anterior, sustituyendo la media de puntos anotados por las columnas 
#       "MEDIA DE ASISTENCIAS REPARTIDAS" y "MEDIA DE REBOTES RECOGIDOS"

# Empezamos recorriendo el array generado
# inicializamos a 0 todas las variables necesarias para los calculos del bucle
max_pts = 0 # Para calcular el numero maximo de puntos, y seleccionar la temporada
min_pts = 0 # Para calcular el numero minimo de puntos, y seleccionar la temporada
total_partidos = 0 # Para calcular la media por partido (tras el bucle)
media_puntos_absoluta = 0 # para calcular la media de puntos 
media_rebotes_absoluta = 0 # para calcular la media de rebotes 
media_asistencias_absoluta = 0 # para calcular la media de asistencias

for i in range(1, len(regular_season_stats)): # Empieza en 1 para saltarnos las cabeceras
    pts_año = regular_season_stats[i][3]
    partidos_año = regular_season_stats[i][2]
    # 1.1 Temporada con el maximo numero de puntos anotados 
    if partidos_año*pts_año > max_pts:
        max_pts = partidos_año*pts_año
        season_max_points = regular_season_stats[i][0]

    # 1.2 Temporada con el minimo numero de puntos anotados
    # Inicializamos el min_pts con el primer cálculo, para tener un valor de referencia (puesto que 0 no va a ser un valor real)
    if(i==1): 
        min_pts = partidos_año*pts_año
        season_min_points = regular_season_stats[i][0]
    elif partidos_año*pts_año < min_pts:
        min_pts = partidos_año*pts_año
        season_min_points = regular_season_stats[i][0]

    # 2. Media absoluta de puntos de toda la carrera
    # Vamos guardando en una variable la suma de partidos totales para calcular la media tras el bucle
    total_partidos += regular_season_stats[i][2]
    # En otra variable guardamos la operacion que debemos realizar para calcular los puntos (suma por temporada)
    media_puntos_absoluta += partidos_año*pts_año

    # 3. Realizamos la misma operacion con los rebotes y asistencias
    media_rebotes_absoluta += partidos_año*regular_season_stats[i][5] # Rebotes en la posicion 5
    media_asistencias_absoluta += partidos_año*regular_season_stats[i][4] # Asistencias en la posicion 4

avg_career_points = media_puntos_absoluta/total_partidos
avg_career_rebounds = media_rebotes_absoluta/total_partidos
avg_career_assists = media_asistencias_absoluta/total_partidos

print("########################################################################################################################")
print(f"La temporada con mayor cantidad total de puntos anotados es {season_max_points}, con un total de {max_pts:.2f} puntos.")
print(f"La temporada con menor cantidad total de puntos anotados es {season_min_points}, con un total de {min_pts:.2f} puntos.")
print(f"La media de puntos durante toda la carrera de Kobe Bryant es de {avg_career_points:.2f} puntos")
print(f"La media de rebotes durante toda la carrera de Kobe Bryant es de {avg_career_rebounds:.2f} rebotes")
print(f"La media de asistencias durante toda la carrera de Kobe Bryant es de {avg_career_assists:.2f} asistencias")
