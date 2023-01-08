import csv

with open("../bad_format.csv") as file:
    # Leer el archivo usando el método csv.reader
    csv_reader = csv.reader(file)
    
    # Obtener la fila de cabeceras
    headers = next(csv_reader)
    print(headers)
    # Iterar sobre las filas del archivo
    for row in csv_reader:
        # Convertir cada valor de la fila a un valor flotante, excepto el primer valor
        row = [row[0]] + [row[1]] + [float(val) for val in row[2:]]
        print(row)
    # dict_reader =csv.DictReader(file)
    # for row in dict_reader:
    #     row = [float(val) for val in row.values]
    #     print(row.values)
    