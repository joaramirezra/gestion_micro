import numpy as np
import pandas as pd

def calculo_escala():
    micro_carac = pd.read_csv("./archivos/calibracion_escala.csv", sep= ";" , encoding= "latin")
    reticulas = micro_carac.iloc[0]["reticulas"]
    mili = micro_carac.iloc[0]["milimetros"]
    escala = mili / reticulas
    return escala

limites_size = [4096,256,64,4,2,1,1/2,1/4,1/8, 1/16, 1/32, 1/64, 1/128, 1/256, 1/2**14,0]
print(limites_size)
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

def perc_comp ():
    conteo = seleccion_conteo()
    

# tamanos = [tama単os[random.randint(0,2)] for x in range (10000)]
# minerales = [mineral[random.randint(0,11)] for x in range (10000)]
# formas = [forma[random.randint(0,3)] for x in range (10000)]

# df = pd.DataFrame({'tama単os' : tamanos,
#                    'minerales' : minerales,
#                    'formas':formas
#                    })
# df

# plt.figure(figsize=(15,5))
# df['formas'].value_counts(dropna=False,normalize = True).sort_index().plot.bar()
# plt.grid(alpha = 0.7)
# plt.title('esto es un histograma'.upper())
# plt.xlabel('minerales')
# plt.ylabel('porcentaje[%]')
# plt.savefig('minerales.jpg')

# for columna in df.columns:
    # plt.figure(figsize=(15,5))
    # df[columna].value_counts(dropna=False,normalize = True).sort_index().plot.bar()
    # plt.grid(alpha = 0.7)
    # plt.title('esto es un histograma'.upper())
    # plt.xlabel('minerales')
    # plt.ylabel('porcentaje[%]')
    # plt.savefig(columna+'.jpg')

# minerales = ['Cuarzo','Plagioclasa','feldespato']
# mask = df['mineral'].isin(minerales)
# df = df[mask]
# tam = df.shape[0]
# df.groupby('mineral')['milimetros'].count()/tam