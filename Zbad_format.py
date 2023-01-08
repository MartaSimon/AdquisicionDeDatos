# Importa la libreria csv para poder usarla
import csv
import re

def load_csv(file_path):
    # Abrimos el archivo con with
    with open(file_path, "r") as input_file:
        reader = csv.reader(input_file , delimiter = ",")
        matrix = [row for row in reader] 
        return matrix

file_path="../bad_format.csv"
matrix = load_csv(file_path)

pts = []
for row in matrix:
    #print(row, len(row))
    # Formateamos las filas para que los numeros con decimales sean 
    #string=re.sub("\(.*?\)","()",string)
    #for item in row:
    #    print(item)
    #    row.append(re.sub("\(.*?\)","", item))
    print(row)
    # obtenemos la penúltima columna, la de los puntos, y la vamos almacenando
    #pts.append(row[-2])
print(pts)



