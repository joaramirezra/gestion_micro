from numpy import NaN, nan
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap

def Crear_Archivo(nombre_archivo):
  titulo = ";".join(archivos[nombre_archivo])+'\n'

  with open("./archivos/"+ nombre_archivo+'.csv','w+') as file :
    file.write(titulo)

def contar_puntos(archivo):
  '''
  configura ( setea ) el numero dentro del lcd display
  '''
  df = pd.read_csv("./archivos/"+ archivo + ".csv", sep=";", encoding= "latin")
  rows = df.shape[0]
  return rows

#-------------------------------------------------------------------------------
def llenado_csv(archivo,datos):
  '''
  Llena los archivos temporales de un solo registro
  '''
  if not validar_exitencia_archivo("./archivos/"+archivo+ ".csv"):
    Crear_Archivo(archivo)

  df = pd.read_csv("./archivos/"+ archivo + ".csv", sep = ";", encoding= "latin")
  
  for i in datos:
    df[i] = datos[i]
  
  df.to_csv("./archivos/" + archivo +".csv",encoding = "latin", sep=';',index=False)

def navegar_archivos():
  ruta_archivo = QFileDialog.getOpenFileName()
  return ruta_archivo[0] 

def agregar_imagen():
  '''
  Funcion encargada de abrir el navegador de archivos para subir una foto al
  programa
  '''
  ruta_archivo = navegar_archivos()
  # if(ruta_archivo.split('.')[-1] in ['jpg,jpeg,png.....'])
  imagen = QPixmap(ruta_archivo)
  imagen_escalada = imagen.scaled(500,250, QtCore.Qt.KeepAspectRatio)
  return ruta_archivo, imagen_escalada

def stack_micro_data():
  if not validar_exitencia_archivo("./archivos/current_micro.csv"):
    Crear_Archivo("current_micro")
  base = pd.read_csv("./archivos/current_micro.csv", sep = ";", encoding= "latin")
  agregar_foto = pd.read_csv("./archivos/auxiliar_micro.csv", sep = ";", encoding= "latin")
  base = pd.concat([base,agregar_foto])
  base.to_csv("./archivos/current_micro.csv", encoding= "latin" ,sep = ";", index = False)

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
             'Diccionario_simbolos':['Simbolo','Mineral', "tipo", "subtipo_1", "subtipo_2" ],
             "current_general" : ["igm","numero_campo",  "unidad_lito", "localidad",  "departamento","municipio", "plancha",
                                  "escala","coor_x", "origen_coor", "coor_y","colector", "fecha_recol", "Intemprete", "Fecha_interp", 
                                  "cantidad_p", "Tipo_r", "Subt_r"],
              "calibracion_escala" : ["reticulas", "milimetros", "objetivo"],
              "current_macro_sed" : ["tipo_roca", "textura", "color", "laminación", "bioturbación",
                        "meteorización", "partición", "prueba_fosfatos", "pureba_HCl", "observaciones", "url_foto", "url_escala"],
              "current_macro": ["observaciones", "url_foto", "url_escala"],
              "current_micro": ["url_ppl", "url_xpl", "descrpcion_micro"],
              'auxiliar_micro': ["url_ppl", "url_xpl", "descrpcion_micro"]}

def continuar_conteo():
  url =  QFileDialog.getOpenFileName()[0]
  if url != "":
    general = pd.read_csv("./archivos/current_general.csv", sep=";", encoding= "latin")
    prev = pd.read_csv(url, sep=";", encoding="latin")
    if general["Subt_r"][0] == "Siliciclástica": archivo = "Conteo_siliciclasticas"
    elif general["Subt_r"][0] == "Calcárea": archivo = "Conteo_calcareas"
    elif general["Subt_r"][0] == "Regional o de Contacto": archivo = "Conteo_regionales"
    elif general["Subt_r"][0] == "Dinámico": archivo = "Conteo_dinamicas"
    elif general["Subt_r"][0] == "Plutónica": archivo = "Conteo_plutonicas"
    elif general["Subt_r"][0] == "Volcánica": archivo = "Conteo_volcanicas"
    else: archivo = "Conteo_volcanoclasticas"
    prev.to_csv("./archivos/" + archivo + ".csv", sep = ";", encoding= "latin", index = False)
    return archivo
  else:
    pass

def crear_los_archivos():
  for archivo in archivos :
    if archivo == 'Diccionario_simbolos':
      continue
    else:
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
  return (lista_minerales[mask]['Mineral'].values[0])

def traducir_tipo(tipo):
  tipos = pd.read_csv("./archivos/Diccionario_simbolos.csv",sep=';', encoding= "latin")
  mask = tipos['tipo'] == tipo
  return (tipos[mask]['tipo'].values[0])

def traducir_subtipo(subtipo):
  subtipos = pd.read_csv("./archivos/Diccionario_simbolos.csv",sep=';', encoding= "latin")
  mask = subtipos['subtipo_1'] == subtipo
  return (subtipos[mask]['Mineral'].values[0])

def agregar_elemento(simbolo,mineral,tipo, subtipo_1):
  df = pd.read_csv("./archivos/Diccionario_simbolos.csv",sep=';')
  if simbolo == "":
    return False
  elif not (validar_simbolo(simbolo)):
    df2 = pd.DataFrame({'Simbolo':[simbolo],
           'Mineral':[mineral],'Tipo':[tipo], 'Subtipo':[subtipo_1]})
    df = pd.concat([df,df2])
    df.to_csv("./archivos/Diccionario_simbolos.csv", encoding= "latin" ,sep = ";", index = False)
    return True
  

def agregar_puntos(archivo, parametros):
  
  if(not validar_exitencia_archivo("./archivos/"+ archivo + ".csv")):
    Crear_Archivo(archivo)
  if validar_simbolo(parametros[0][0]): # valida que el simbolo este en lista
    mineral = traducir_simbolo(parametros[0][0])
    tipo= traducir_tipo(parametros [0][0])
    subtipo= traducir_subtipo(parametros [0][0])
    parametros[0][0] = mineral
    parametros.append([tipo,subtipo])
    diccionario = dict(zip(archivos[archivo], parametros))
    data = pd.read_csv("./archivos/"+archivo+".csv",sep=';', encoding= "latin")
    punto = pd.DataFrame(diccionario)
    data = pd.concat([data,punto])
    data.to_csv('./archivos/'+ archivo + ".csv",encoding= "latin", sep=';',index=False)
    return True
  else:
    return False

def guardar_csv():
  general = pd.read_csv("./archivos/current_general.csv", sep = ";", encoding= "latin")
  if general["Tipo_r"][0] != "Sedimentaria":
    macro = pd.read_csv("./archivos/current_macro_sed.csv", sep= ";", encoding= "latin")
  else:
    macro = pd.read_csv("./archivos/current_macro_sed.csv", sep= ";", encoding= "latin")
  if general["Subt_r"][0] == "Siliciclástica": conteo = pd.read_csv("./archivos/Conteo_siliciclasticas.csv", sep = ";", encoding= "latin")
  elif general["Subt_r"][0] == "Calcárea": conteo = pd.read_csv("./archivos/Conteo_calcareas.csv", sep = ";", encoding= "latin")
  elif general["Subt_r"][0] == "Regional o de Contacto": conteo = pd.read_csv("./archivos/Conteo_regionales.csv", sep = ";", encoding= "latin")
  elif general["Subt_r"][0] == "Dinámico": conteo = pd.read_csv("./archivos/Conteo_dinamicas.csv", sep = ";", encoding= "latin")
  elif general["Subt_r"][0] == "Plutónica": conteo = pd.read_csv("./archivos/Conteo_plutonicas.csv", sep = ";", encoding= "latin")
  elif general["Subt_r"][0] == "Volcánica": conteo = pd.read_csv("./archivos/Conteo_volcanicas.csv", sep = ";", encoding= "latin")
  elif general["Subt_r"][0] == "Volcanoclástica": conteo = pd.read_csv("./archivos/Conteo_volcanoclasticas.csv", sep = ";", encoding= "latin")
  micro = pd.read_csv("./archivos/current_micro.csv", sep= ";", encoding="latin")
  name = str(general["numero_campo"][0])
  nombre_archivo = QFileDialog.getSaveFileName(directory= name,filter= " csv (*.csv)")[0]
  conteo.to_csv(nombre_archivo,encoding= "latin", sep=';',index=False)
  opciones = ["_macro", "_general","_micro"]
  for i in opciones:
    print(i)
    lista = nombre_archivo.split("/")
    name = lista[-1]
    name_sp = name.split(".")
    name_sp[0] = name_sp[0] + i
    name2 = ".".join(name_sp)
    lista[-1] = name2
    ruta_mac = "/".join(lista)
    if i == "_macro": macro.to_csv(ruta_mac,encoding= "latin", sep=';',index=False)
    elif i == "_general" : general.to_csv(ruta_mac,encoding= "latin", sep=';',index=False)
    else: micro.to_csv(ruta_mac,encoding= "latin", sep=';',index=False)


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