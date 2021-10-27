import numpy as np
import pandas as pd
from pandas.core import groupby
from funciones.fijar_datos import contar_puntos
# from ternarios import *
from funciones.ternarios import *
from numpy import NaN, average, nan

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
    redond = []
    esfer = []
    df_count = conteo.loc[conteo["nombres_grano"] != "nulo"]
    tam_c = df_count.shape[0]
    promedios = []

    for i in sizes:
        grava = conteo.loc[conteo["nombres_grano"].isin(i)]
        tam = grava.shape[0]
        if tam > 0:
            if grava["redondez"].mode()[0] != "---------------":
                redond.append(grava["redondez"].mode()[0])
            else:
                redond.append("N/A")
            if grava["esfericidad"].mode()[0] != "---------------":
                esfer.append(grava["esfericidad"].mode()[0])
            else:
                esfer.append("N/A")
            avr = grava["milimetros"].mean()
            if avr > 0:
                promedios.append(str(round(avr, 2)))
            else:
                promedios.append("N/A")
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
    names = list(df_percs.index)
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
    tam = conteo.shape[0]
    lodo = ["Limo grueso", "Limo medio", "Limo fino", "Limo muy fino", "Arcilla", "Coloide", "nulo"]
    sp_arci = lambda x : 'arcilloso' if (x in lodo) else "grano"
    conteo['nombres_grano'] = conteo["milimetros"].apply(traduccion_grano)
    conteo["soporte"] = conteo["nombres_grano"].apply(sp_arci)
    conteo.loc[conteo.Subtipo == "Primaria", 'soporte'] = "Primaria"
    conteo.loc[conteo.Subtipo == "Secundaria", 'soporte'] = "Secundaria"
    df_percs = conteo.groupby("soporte")["Mineral"].count()/tam
    percs = df_percs.tolist()
    percs = rounder(percs)
    names = list(df_percs.index)
    data = dict(zip(names, percs))
    soportes = ["grano", "arcilloso", "Primaria", "Secundaria"]
    poros = ["Primaria", "Secundaria"]
    for i in soportes:
        try:
            data[i] = round(data[i],2)
        except:
            data[i] = str(0.00)
    data["Porosidad"] = 0.00
    for i in poros:
        try:
            data["Porosidad"] = round(data["Porosidad"] + data[i], 2)
        except:
            pass
    for i in data:
        data[i] = str((data[i]))
    return data


def simplificacion_conteo():
    conteo = pd.read_csv("./archivos/Conteo_siliciclasticas.csv", sep = ";", encoding= "latin")
    escala = calculo_escala()
    conteo["milimetros"] = conteo["Size"] * escala
    conteo['nombres_grano'] = conteo["milimetros"].apply(traduccion_grano)
    conteo = conteo.loc[conteo["nombres_grano"] != "nulo"]
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
    df['nombres_grano'] = df['nombres_grano'].apply(reducir_limo)
    df['nombres_grano'] = df['nombres_grano'].apply(upcase)
    tam = df.shape[0]
    var = df.groupby('nombres_grano')['milimetros'].count()/tam
    names = list(var.index)
    percs = var.tolist()
    try:
        for i in range(len(percs)):
            percs[i] = percs[i]*100
        rounder(percs)
    except:
        pass
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
    try:
        first = names[0]
        for i in data:
            if data[i] > data[first]:
                redondez = i
                first = i
            else:
                redondez = first
    except:
        pass
    redond = conteo.groupby("esfericidad")["Mineral"].count()/size
    names = list(redond.index)
    percs = redond.tolist()
    data = dict(zip(names,percs))
    try:

        first = names[0]
        for i in data:
            if data[i] > data[first]:
                esfericidad = i
                first = i
            else:
                esfericidad = first
    except:
        pass
    return redondez, esfericidad


def grano_critalinas(milimetros):
    sizes = ["Muy Grueso", "Grueso", "Medio", "Fino", "Muy fino", "Ultra fino"]
    limites_size = [4096,16,4,1,0.1, 0.01, 0]
    for i in range(len(sizes)):
        if limites_size[i] >= milimetros > limites_size[i+1]:
            return sizes[i]

def datos_plut():
    df = pd.read_csv("./archivos/Conteo_plutonicas.csv", sep = ";", encoding= "latin")
    tam = df.shape[0]
    lista = ["---------------", "Principal", "Accesorio", "Alteracion", "Introduccion"]
    for i in lista:
        filtrado = df[df['Tipo']== i]
        df_percs = filtrado.groupby(["Mineral"])["Ternarios"].count()/tam
        print(df_percs)  
   

def datos_silic():
    conteo = pd.read_csv("./archivos/Conteo_siliciclasticas.csv", sep = ";", encoding= "latin")
    del conteo["observaciones"]
    escala = calculo_escala()
    reemplazo = ["Materia org.", "Cemento","Otros ortoq."]
    for i in reemplazo:
        conteo.loc[conteo["Tipo"] == i, "Subtipo"] = i
    no_p = conteo.loc[conteo["Tipo"] != "Porosidad"]
    tam = no_p.shape[0]
    df_percs = no_p.groupby("Subtipo")["Ternarios"].count()/tam
    no_p["milim"] = no_p["Size"] * escala
    df2 = no_p.groupby("Subtipo")["milim"].mean()
    avera_mm = df2.tolist()
    titles =list (df_percs.index)
    percs = df_percs.tolist()
    for i in range(len(percs)):
        percs[i] = percs[i] * 100
    percs = rounder(percs)
    data = dict(zip(titles, percs))
    promedios_tam = dict(zip(titles, avera_mm))
    

    campos_form = ["Metamorficos", "Volcanicos", "Plutonicos", "Sedimentarios",
                   "Cuarzo mono", "Cuarzo poli", "Chert", "Feldespato K", "Feldespato Na - Ca", "Micas",
                   "Min. arcillosos", "Granos aloq.", "Otros terrigenos", "Opacos", "Materia org.",
                   "Cemento", "Otros ortoq.", "Porosidad", "Cuarzo", "Liticos", "Feldespato","Terrigenos"]
    feldes = ["Feldespato K", "Feldespato Na - Ca"]
    litic = ["Metamorficos", "Volcanicos", "Plutonicos", "Sedimentarios"]
    quartz = ["Cuarzo mono", "Cuarzo poli"]
    complete = ["Cuarzo", "Liticos", "Feldespato", "Terrigenos"]
    terrig = ["Cuarzo mono", "Cuarzo poli", "Chert", "Feldespato K", "Feldespato Na - Ca", "Micas",
              "Min. arcillosos", "Granos aloq.", "Otros terrigenos", "Opacos"]
    esfer =[]
    redond = []
    for i in complete:
        data[i] = 0.00
        promedios_tam[i] = 0.00

    for i in feldes:
        try:
            data["Feldespato"] += data[i]
            promedios_tam["Feldespato"] += promedios_tam[i]
        except:
            continue

    for i in quartz:
        try:
            data["Cuarzo"] += data[i]
            promedios_tam["Cuarzo"] += promedios_tam[i]
        except:
            continue
    for i in litic:
        try:
            data["Liticos"] += data[i]
            promedios_tam["Liticos"] += promedios_tam[i]
        except:
            continue
    for i in terrig:
        try:
            data["Terrigenos"] += data[i]
            promedios_tam["Terrigenos"] += promedios_tam[i]
        except:
            continue
    for i in campos_form:
        try:
            data[i] = str(data[i])
            if promedios_tam[i] == 0.00:
                promedios_tam[i] = "N/A"
            else:
                promedios_tam[i] = str(round(promedios_tam[i], 2))
        except:
            data[i] = str(0.00)
            promedios_tam[i] = "N/A"
        try:
            df3 = conteo.loc[conteo["Subtipo"] == i]
            if df3["redondez"].mode()[0] != "---------------":
                redond.append(df3["redondez"].mode()[0])
            if df3["esfericidad"].mode()[0] != "---------------":
                esfer.append(df3["esfericidad"].mode()[0])
        except:
            redond.append("N/A")
            esfer.append("N/A")
    redond_p = dict(zip(campos_form, redond))
    esfer_p = dict(zip(campos_form, esfer))
    return data, promedios_tam, redond_p, esfer_p


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

def histograma_mineral():
    data=seleccion_conteo()
    data['Mineral'].value_counts().plot.bar()
    plt.xticks(rotation=45)
    plt.title('Histograma mineral')
    plt.show()

def histograma_size():
    data=seleccion_conteo()
    data['Size']=data['Size'].apply(traduccion_grano)
    data['Size'].value_counts().plot.bar()
    plt.xticks(rotation=45)
    plt.title('Histograma tamaño')
    plt.show()

