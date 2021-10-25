import numpy as np
import pandas as pd
from ternarios import *
#from funciones.ternarios import *
from numpy import NaN, nan


def calculo_escala():
    micro_carac = pd.read_csv("./archivos/calibracion_escala.csv", sep= ";" , encoding= "latin")
    reticulas = micro_carac.iloc[0]["reticulas"]
    mili = micro_carac.iloc[0]["milimetros"]
    escala = mili / reticulas
    return escala

limites_size = [4096,256,64,4,2,1,1/2,1/4,1/8, 1/16, 1/32, 1/64, 1/128, 1/256, 1/2**14,0]


def traduccion_grano(milimetros):
    limites_size = [4096,256,64,4,2,1,1/2,1/4,1/8, 1/16, 1/32, 1/64, 1/128, 1/256, 1/2**14,0]
    sizes = ["Bloque", "Guijo", "Guijarro", "Granulo", "Arena muy gruesa", "Arena gruesa",
            "Arena media", "Arena fina", "Arena muy fina", "Limo grueso", "Limo medio", 
            "Limo fino", "Limo muy fino", "Arcilla", "Coloide"]
    for i in range(len(sizes)):
        if limites_size[i] >= milimetros > limites_size[i+1]:
            return sizes[i]

def seleccion_conteo():
    general = pd.read_csv("./archivos/current_general.csv", sep = ";", encoding= "latin") 
    if general["Subt_r"][0] == "Siliciclástica": conteo = pd.read_csv("./archivos/Conteo_siliciclasticas.csv", sep = ";", encoding= "latin")
    elif general["Subt_r"][0] == "Calcárea": conteo = pd.read_csv("./archivos/Conteo_calcareas.csv", sep = ";", encoding= "latin")
    elif general["Subt_r"][0] == "Regional o de Contacto": conteo = pd.read_csv("./archivos/Conteo_regionales.csv", sep = ";", encoding= "latin")
    elif general["Subt_r"][0] == "Dinámico": conteo = pd.read_csv("./archivos/Conteo_dinamicas.csv", sep = ";", encoding= "latin")
    elif general["Subt_r"][0] == "Plutónica": conteo = pd.read_csv("./archivos/Conteo_plutonicas.csv", sep = ";", encoding= "latin")
    elif general["Subt_r"][0] == "Volcánica": conteo = pd.read_csv("./archivos/Conteo_volcanicas.csv", sep = ";", encoding= "latin")
    else: conteo = pd.read_csv("./archivos/Conteo_volcanoclasticas.csv", sep = ";", encoding= "latin")
    return conteo

def simplificacion_conteo():
    conteo = seleccion_conteo()
    escala = calculo_escala()
    conteo["milimetros"] = conteo["Size"] * escala
    conteo['nombres_grano'] = conteo["milimetros"].apply(traduccion_grano)
    df = conteo[["Mineral","milimetros",'nombres_grano']]
    promedio_total = df['milimetros'].apply('mean')
    av_size = traduccion_grano(promedio_total)
    df.dropna(inplace=True)
    tam = df.shape[0]
    df.groupby('nombres_grano')['milimetros'].count()/tam

    gravas = ["Boloque", "Guijo", "Guijarro", "Granulo"]
    arena = ["Arena muy gruesa", "Arena gruesa", "Arena media", "Arena fina", "Arena muy fina"]
    lodo = ["Limo grueso", "Limo medio", "Limo fino", "Limo muy fino", "Arcilla"]

    reducir_grava = lambda x : 'GRAVA' if (x in gravas) else x
    reducir_arena = lambda x : 'ARENA' if (x in arena) else x
    reducir_lodo = lambda x : "LODO" if (x in lodo) else x
    reducir_limo = lambda x : "LIMO" if (x in lodo) else x
    upcase = lambda x : x.upper()

    df['nombres_grano'] = df['nombres_grano'].apply(reducir_grava)
    df['nombres_grano'] = df['nombres_grano'].apply(reducir_arena)
    if (df['nombres_grano'] == "GRAVA").sum() > 0:
        df['nombres_grano'] = df['nombres_grano'].apply(reducir_lodo)
        
    else:
        df['nombres_grano'] = df['nombres_grano'].apply(reducir_limo)
        df['nombres_grano'] = df['nombres_grano'].apply(upcase)

    tam = df.shape[0]
    percs = []
    var = df.groupby('nombres_grano')['milimetros'].count()/tam
    names = df["nombres_grano"].unique().tolist()
    names.sort()
    for i in range(len(var)):
        percs.append(var[i])
    data = dict(zip(names,percs))
    return data

def datos_silic():
    conteo = seleccion_conteo()
    filtro= conteo[conteo['Ternarios'].isin(['2','3'])].copy()
    del conteo["observaciones"]
    print(conteo)
    tam = conteo.shape[0]
    reemplazo = ["Materia org.", "Cemento","Otros ortoq."]
    for i in reemplazo:
        conteo.loc[conteo["Tipo"] == i, "Subtipo"] = i
    print(conteo)
    df_percs = conteo.groupby("Subtipo")["Ternarios"].count()/tam
    print(df_percs)
    df2 = conteo.groupby("Tipo")["Subtipo"].count()/tam
    titles =list (df_percs.index)
    percs = df_percs.tolist()
    for i in range(len(percs)):
        percs[i] = percs[i] * 100
    percs = rounder(percs)
    total = 0
    for i in percs:
        total += i
    data = dict(zip(titles, percs))
    
    return data

def grano_critalinas(milimetros):
    sizes = ["Muy Grueso", "Grueso", "Medio", "Fino", "Muy fino", "Ultra fino"]
    limites_size = [4096,16,4,1,0.1, 0.01, 0]
    for i in range(len(sizes)):
        if limites_size[i] >= milimetros > limites_size[i+1]:
            return sizes[i]

def simplificacion_comp():
    conteo = seleccion_conteo()
    df = conteo[["Mineral"],["Size"]]
    df.dropna(inplace=True)
    tam = df.shape[0]
    return tam 

def conteo_normalizado(df):
  tam = df.shape[0]
  var = df.groupby('Ternarios')['Mineral'].count()/tam
  return var

def conteo_normalizado_filtrado(df,lista_elementos):
  filtrado = df[df['Ternarios'].isin(lista_elementos)]
  return conteo_normalizado(filtrado)

def normal_select(df,general):
    tam = df.shape[0]
    var= df.groupby('Ternarios')['Mineral'].count()/tam
    if(general == 'Siliciclástica'):
        lista = ['Cuarzo','Feldespato k','Plagioclasa']
    elif(general == 'Plutónica'):
        try:
            a=var['Feldespatoide']
            lista = ['Feldespatoide','Feldespato k','Plagioclasa']
        except:
            try:
                a=var['Olivino']
                if a>0.05 :
                    try:
                        if var['Plagioclasa'] >0:
                            lista=['Ortopiroxeno','Clinopiroxeno','Olivino','Plagioclasa']
                    except:
                        try:
                            if var['Hornblenda'] >0:
                                lista= ['Ortopiroxeno','Clinopiroxeno','Olivino','Hornblenda']
                        except:
                            lista = ['Ortopiroxeno','Clinopiroxeno','Olivino']
                else:
                    lista = ['Cuarzo','Feldespato k','Plagioclasa']
            except:
                try:
                    a=var['Ortopiroxeno']
                    try:
                        if var['Cuarzo']<0.05:
                            lista= ['Ortopiroxeno','Clinopiroxeno','Plagioclasa']
                        else:
                            lista = ['Cuarzo','Feldespato k','Plagioclasa']
                    except:
                        lista= ['Ortopiroxeno','Clinopiroxeno','Plagioclasa','Hornlenda']
                except:
                    try:
                        a=var['Clinopiroxeno']
                        lista = ['Clinopiroxeno','Plagioclasa','Hornlenda']
                    except:
                        lista = ['Cuarzo','Feldespato k','Plagioclasa']
    return lista

def perc_comp ():
    conteo = seleccion_conteo()
    general = pd.read_csv("./archivos/current_general.csv", sep= ";" , encoding= "latin")
    tipo_r= general["Subt_r"][0]
    nc = str(general.iloc[0]["numero_campo"])
    if nc == nan: nc = "Numero de campo"
    lista= normal_select(conteo,tipo_r)
    var= conteo_normalizado_filtrado(conteo,lista)
    #suma=var['Clinopiroxeno']+ var['Clinopiroxeno'] #pdte
    percs=[]
    for i in range(len(var)):
        percs.append(var[i]*100)
    percs.append(nc) 
    print (var)
    print (percs)
    return percs
lista_aux=perc_comp()
lista_n= [lista_aux[1],lista_aux[0],lista_aux[2],lista_aux[3]]
streck76_QAP(lista_n)
