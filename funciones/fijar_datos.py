from PyQt5.sip import enableautoconversion
from numpy import NaN, nan
import pandas as pd

def Crear_Archivo(nombre_archivo):
  titulo = ";".join(archivos[nombre_archivo])+'\n'

  with open("./archivos/"+ nombre_archivo+'.csv','w+') as file :
    file.write(titulo)

def llenado_archivos(archivo,datos):
  if not validar_exitencia_archivo(archivo):
    Crear_Archivo(archivo)

  df = pd.read_csv("./archivos/"+ archivo + ".csv", sep = ";", encoding= "latin")
  for i in datos:
    df[i] = datos[i]
  df.to_csv("./archivos/" + archivo +".csv",encoding = "latin", sep=';',index=False)


archivos =  {'Conteo_siliciclasticas':['Mineral','Size','redondez','esfericidad',
                                     'tipo_contacto','observaciones'],
             'Conteo_calcareas':['Mineral','Size','redondez','esfericidad',
                                     'tipo_contacto','observaciones'],
              "Conteo_plutonicas": ["Mineral", "Size", "Forma", "Genesis", "Observaciones"],
              "Conteo_volcanicas": ["Mineral", "Size", "Forma", "Observaciones"],
              "Conteo_volcanoclasticas": ['Mineral','Size','redondez','esfericidad',
                                     'Tipo_contacto',"Tipo_fragmento",'observaciones'],
              "Conteo_dinamicas": ["Mineral","Tipo", "Size", "Forma", "Borde", "Geometria_borde", "Observaciones"],
              "Conteo_regionales": ["Mineral","Size", "Forma", "Borde", "Geometria_borde", "Observaciones"],
             'Diccionario_simbolos':['Simbolo','Mineral'],
             "current_general" : ["Intemprete", "Fecha_interp", "Tipo_r", "Subt_r", "igm", "numero_campo", "unidad_lito", "localidad", "departamento", "municipio",
                                  "plancha", "escala", "coor_x", "origen_coor", "coor_y", "colector", 
                                  "fecha_recol", "cantidad_p"],
              "calibracion_escala" : ["reticulas", "milimetros", "objetivo"],
              ""
              "current_macro" : ["tipo_roca", "textura", "color", "laminación", "bioturbacion",
                        "meteorizacion", "particion", "prueba_fosfatos", "pureba_HCl", "observaciones"]}

def crear_los_archivos():
  for archivo in archivos :
    titulo = ";".join(archivos[archivo])+'\n'

    with open( "./archivos/" +archivo+'.csv','w+') as file :
      file.write(titulo)


def validar_exitencia_archivo(nombre_archivo):
  try:
    with open(nombre_archivo,'r') as file:
      return True
  except:
    return False

def validar_simbolo(simbolo):
  lista_simbolos = pd.read_csv("./archivos/Diccionario_simbolos.csv",sep=';', encoding= "latin")
  return (lista_simbolos['Simbolo'] == simbolo).sum()

def traducir_simbolo(simbolo):
  lista_minerales = pd.read_csv("./archivos/Diccionario_simbolos.csv",sep=';', encoding= "latin")
  mask = lista_minerales['Simbolo'] == simbolo
  return lista_minerales[mask]['Mineral'].values[0]

def agregar_elemento(simbolo,mineral):
  df = pd.read_csv("./archivos/Diccionario_simbolos.csv",sep=';')
  if simbolo == "":
    return False
  elif not (validar_simbolo(simbolo)):
    df2 = pd.DataFrame({'Simbolo':[simbolo],
           'Mineral':[mineral]})
    df = pd.concat([df,df2])
    df.to_csv("./archivos/Diccionario_simbolos.csv", encoding= "latin" ,sep = ";", index = False)
    return True
  

def agregar_puntos(archivo, parametros):
  
  if(not validar_exitencia_archivo("./archivos/"+ archivo + ".csv")):
    Crear_Archivo(archivo)
  if validar_simbolo(parametros[0][0]):
    mineral = traducir_simbolo(parametros[0][0])
    parametros[0][0] = mineral
    diccionario = dict(zip(archivos[archivo], parametros))
    data = pd.read_csv("./archivos/"+archivo+".csv",sep=';', encoding= "latin")
    punto = pd.DataFrame(diccionario)
    data = pd.concat([data,punto])
    data.to_csv('./archivos/'+ archivo + ".csv",encoding= "latin", sep=';',index=False)
    return True
  else:
    return False

# def agregar_punto_siliciclastica(simbolo,size,rendondez,esfericidad,tipo_contacto,observaciones):
#   if(not validar_exitencia_archivo('./archivos/Conteo_siliciclasticas.csv')):
#     Crear_Archivo('Conteo_siliciclasticas')
#   if validar_simbolo(simbolo):
#     mineral = traducir_simbolo(simbolo)
#     data = pd.read_csv('./archivos/Conteo_siliciclasticas.csv',sep=';')
#     punto = pd.DataFrame({'Mineral':[mineral],
#                             'Size':[size],
#                             'redondez':[rendondez],
#                             'esfericidad':[esfericidad],
#                             'tipo_contacto':[tipo_contacto],
#                             'observaciones':[observaciones]
#                             }
#                         )
#     data = pd.concat([data,punto])
#     data.to_csv('./archivos/Conteo_siliciclasticas.csv',sep=';',index=False)
#     return True
#   else:
#     return False

# def agregar_punto_silicilastica(mineral, size, redondez, esfericidad, tipo_contacto, observaciones):
#   data = pd.read_csv("./archivos/conteo_sedimentarias.csv")
#   punto = pd.DataFrame({"Mineral"})
#   data = pd.concat(data, punto)
#   data.to_csv("")


# def agragar_interfaz(simbolo, etc):
  
# # def guardar_punto(*valores):
# #     with open('./archivos/puntos.csv', 'a+') as file:
# #         file.write(";".join(valores)+'\n')

# # def ultimo_valor():
# #     df = pd.read_csv('./archivos/puntos.csv',sep= ';')
# #     return df.tail(1)


# # def cantidad_puntos():
# #     df = pd.read_csv('./archivos/puntos.csv',sep= ';')
# #     return df.shape[0]

    
# parametros = ['mineral', 'tamaño', 'esfericidad', 'redondez', 'coor_x', 'coor_y']
# dato_conteo = ["Qz", "6", "5", "5", "1", "5"]
# crear_archivo(nombre, parametros)
# escribir_archivo(nombre, dato_conteo)