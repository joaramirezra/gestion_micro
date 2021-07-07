import pandas as pd
def crear_archivo(nombre,parametros):
    with open(nombre, "w+") as file:
        file.write(";".join(parametros) + "\n")

def escribir_archivo(nombre,parametros):
    parametros = map(str, parametros)
    with open(nombre , "a+") as file:
        file.write(";".join(parametros) + "\n")

def leer_archivo(nombre):
    archivo = pd.read_csv(nombre, sep = ";")
    return archivo
nombre = "./archivos/muestra.csv"

# print(leer_archivo(nombre).shape[0])        
parametros = ['mineral', 'tamaño', 'esfericidad', 'redondez', 'coor_x', 'coor_y']
# dato_conteo = ["Qz", "6", "5", "5", "1", "5"]
crear_archivo(nombre, parametros)
# escribir_archivo(nombre, dato_conteo)

