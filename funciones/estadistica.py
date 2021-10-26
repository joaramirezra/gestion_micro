import numpy as np
import pandas as pd
#from ternarios import *
from funciones.ternarios import *
from numpy import NaN, nan

def rounder (perc_list):
    total = 0
    for i in range(len(perc_list)):
        perc_list[i] = round(perc_list[i],2)
        total += perc_list[i]
    if total > 100.00:
        while round(total,2) > 100.00:
            a = np.random.randint(len(perc_list))
            perc_list[a] -= 0.01
            total -= 0.01
    else:
        while round(total,2) < 100.00:
            a = np.random.randint(len(perc_list))
            perc_list[a] += 0.01
            total += 0.01
    total = 0
    for i in range(len(perc_list)):
        perc_list[i] = round(perc_list[i],2)
        total += perc_list[i]
    return perc_list

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
    conteo = pd.read_csv("./archivos/Conteo_siliciclasticas.csv", sep = ";", encoding= "latin")
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
    limo =["Limo grueso", "Limo medio", "Limo fino", "Limo muy fino"]

    reducir_grava = lambda x : 'GRAVA' if (x in gravas) else x
    reducir_arena = lambda x : 'ARENA' if (x in arena) else x
    reducir_lodo = lambda x : "LODO" if (x in lodo) else x
    reducir_limo = lambda x : "LIMO" if (x in limo) else x
    upcase = lambda x : x.upper()

    df['nombres_grano'] = df['nombres_grano'].apply(reducir_grava)
    df['nombres_grano'] = df['nombres_grano'].apply(reducir_arena)
    if (df['nombres_grano'] == "GRAVA").sum() > 0:
        df['nombres_grano'] = df['nombres_grano'].apply(reducir_lodo)
        
    else:
        df['nombres_grano'] = df['nombres_grano'].apply(reducir_limo)
        df['nombres_grano'] = df['nombres_grano'].apply(upcase)

    tam = df.shape[0]
    var = df.groupby('nombres_grano')['milimetros'].count()/tam
    names = list(var.index)
    percs = var.tolist()
    percs = rounder(percs)
    data = dict(zip(names,percs))
    campos = ["ARENA", "GRAVA", "LODO", "LIMO" , "ARCILLA"]
    for i in campos:
        try:
            data[i] = str(data[i])
        except:
            data[i] = str(0.00)
    return data, av_size

def redondez_p():
    conteo = pd.read_csv("./archivos/Conteo_siliciclasticas.csv", sep = ";", encoding= "latin")
    size = conteo.shape[0]
    redond = conteo.groupby("redondez")["Mineral"].count()/size
    names = list(redond.index)
    percs = redond.tolist()
    data = dict(zip(names,percs))
    first = names[0]
    for i in data:
        if data[i] > data[first]:
            redondez = i
            first = i
        else:
            redondez = first
    redond = conteo.groupby("esfericidad")["Mineral"].count()/size
    names = list(redond.index)
    percs = redond.tolist()
    data = dict(zip(names,percs))
    first = names[0]
    for i in data:
        if data[i] > data[first]:
            esfericidad = i
            first = i
        else:
            esfericidad = first
    
    return redondez, esfericidad



def grano_critalinas(milimetros):
    sizes = ["Muy Grueso", "Grueso", "Medio", "Fino", "Muy fino", "Ultra fino"]
    limites_size = [4096,16,4,1,0.1, 0.01, 0]
    for i in range(len(sizes)):
        if limites_size[i] >= milimetros > limites_size[i+1]:
            return sizes[i]

    

def datos_silic():
    conteo = conteo = pd.read_csv("./archivos/Conteo_siliciclasticas.csv", sep = ";", encoding= "latin")
    del conteo["observaciones"]
    escala = calculo_escala()
    tam = conteo.shape[0]
    reemplazo = ["Materia org.", "Cemento","Otros ortoq."]
    for i in reemplazo:
        conteo.loc[conteo["Tipo"] == i, "Subtipo"] = i
    df_percs = conteo.groupby("Subtipo")["Ternarios"].count()/tam
    conteo["milim"] = conteo["Size"] * escala
    df2 = conteo.groupby("Subtipo")["milim"].mean()
    avera_mm = df2.tolist()
    titles =list (df_percs.index)
    percs = df_percs.tolist()
    for i in range(len(percs)):
        percs[i] = percs[i] * 100
    percs = rounder(percs)
    data = dict(zip(titles, percs))
    promedios_tam = dict(zip(titles, avera_mm))
    df3 = conteo.loc[conteo["Subtipo"] == "Hola"]

    return data, promedios_tam


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
        lista = ["Cuarzo", "Litico volcanico", "Litico plutonico", "Litico metamorfico", 
                     "Litico sedimentario", "Plagioclasa","Feldespato k"]
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
    percs=[]
    for i in range(len(var)):
        percs.append(var[i]*100)
    titles =list (var.index)
    data = dict(zip(titles, percs))
    data['label']=nc
    print (var)
    print (data)
    return data


#perc_comp ()
# lista_aux=perc_comp()
# lista_n= [lista_aux[1],lista_aux[0],lista_aux[2],lista_aux[3]]
# streck76_QAP(lista_n)
