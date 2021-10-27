import numpy as np
import pandas as pd
from funciones.fijar_datos import contar_puntos
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

def traduccion_grano(milimetros):
    limites_size = [4096,256,64,4,2,1,1/2,1/4,1/8, 1/16, 1/32, 1/64, 1/128, 1/256, 1/2**14,0]
    sizes = ["Bloque", "Guijo", "Guijarro", "Granulo", "Arena muy gruesa", "Arena gruesa",
            "Arena media", "Arena fina", "Arena muy fina", "Limo grueso", "Limo medio", 
            "Limo fino", "Limo muy fino", "Arcilla", "Coloide"]
    for i in range(len(sizes)):
        if limites_size[i] >= milimetros > limites_size[i+1]:
            return sizes[i]
    return "nulo"

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

def promedios_silic():
    conteo = conteo = pd.read_csv("./archivos/Conteo_siliciclasticas.csv", sep = ";", encoding= "latin")
    escala = calculo_escala()
    conteo["milimetros"] = conteo["Size"] * escala
    conteo['nombres_grano'] = conteo["milimetros"].apply(traduccion_grano)
    gravas = ["Boloque", "Guijo", "Guijarro", "Granulo"]
    arena = ["Arena muy gruesa", "Arena gruesa", "Arena media", "Arena fina", "Arena muy fina"]
    lodo = ["Limo grueso", "Limo medio", "Limo fino", "Limo muy fino", "Arcilla"]
    limo =["Limo grueso", "Limo medio", "Limo fino", "Limo muy fino"]
    sizes = [gravas, arena, lodo, limo, ["Arcilla"]]
    promedios = []
    redond = []
    esfer = []
    for i in sizes:
        grava = conteo.loc[conteo["nombres_grano"].isin(i)]
        tam = grava.shape[0]
        if tam > 0:
            av= str(round(grava["milimetros"].sum()/tam,2))
            promedios.append(av)
            if conteo["redondez"].mode()[0] != "---------------":
                redond.append(conteo["redondez"].mode()[0])
            else:
                redond.append("N/A")
            if conteo["esfericidad"].mode()[0] != "---------------":
                esfer.append(conteo["esfericidad"].mode()[0])
        else:
            av = "N/A"
            promedios.append(av)
            redond.append(av)
            esfer.append(av)
    return promedios, redond, esfer

def contactos_sed():
    conteo = pd.read_csv("./archivos/Conteo_siliciclasticas.csv", sep = ";", encoding= "latin")
    contactos = ["Flotante", "Tangencial", "Longitudinal", "Concavo-Convexo", "Suturado"]
    tam = conteo.shape[0]
    contact = conteo.loc[conteo["tipo_contacto"] != "---------------" ]
    df_percs = contact.groupby("tipo_contacto")["Mineral"].count()/tam
    percs = df_percs.tolist()
    names = df_percs.index
    data = dict(zip(names, percs))
    for i in contactos:
        try:
            data[i] = str(data[i])
        except:
            data[i] = str(0.00)
    return data

def soporte_g():
    conteo = pd.read_csv("./archivos/Conteo_siliciclasticas.csv", sep = ";", encoding= "latin")
    escala = calculo_escala()
    conteo["milimetros"] = conteo["Size"] * escala
    lodo = ["Limo grueso", "Limo medio", "Limo fino", "Limo muy fino", "Arcilla"]
    sp_arci = lambda x : 'arcilloso' if (x in lodo) else "grano"
    conteo['nombres_grano'] = conteo["milimetros"].apply(traduccion_grano)
    conteo["soporte"] = conteo["nombres_grano"].apply(sp_arci)
    tam = conteo.shape[0]
    df_percs = conteo.groupby("soporte")["Mineral"].count()/tam
    percs = df_percs.tolist()
    percs = rounder(percs)
    names = df_percs.index
    data = dict(zip(names, percs))
    soportes = ["grano", "arcilloso"]
    for i in soportes:
        try:
            data[i] = str(round(data[i],2))
        except:
            data[i] = str(0.00)
    return data

def simplificacion_conteo():
    conteo = pd.read_csv("./archivos/Conteo_siliciclasticas.csv", sep = ";", encoding= "latin")
    escala = calculo_escala()
    conteo["milimetros"] = conteo["Size"] * escala
    conteo['nombres_grano'] = conteo["milimetros"].apply(traduccion_grano)
    av_size = conteo["nombres_grano"].mode()[0]
    df = conteo[["Mineral","milimetros",'nombres_grano']]
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
    data = dict(zip(names,percs))
    campos = ["ARENA", "GRAVA", "LODO", "LIMO" , "ARCILLA"]
    lodos = ["LIMO", "ARCILLA"]
    for i in lodos:
        try:
            data[i] = round(data[i],2)
        except:
            data[i] = 0.00
    data["LODO"] = data["LIMO"] + data["ARCILLA"]
    for i in campos:
        try:
            data[i] = str(round(data[i]))
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
    return data

def histogramas():
  y=simplificacion_conteo()
  plt.style.use('ggplot')
  plt.hist(y)
  plt.show()
 

