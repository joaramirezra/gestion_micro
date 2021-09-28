
import mplstereonet as mpl
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import ternary as tr

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
    print(var)
    print(data)

simplificacion_conteo()

def intersec(line_ini,line_end,corte):
    if len(line_ini) < 3:
        line_ini.append(100-line_ini[0] - line_ini[1]) 
    if len(line_end) < 3:
        line_end.append(100-line_end[0] - line_end[1])
    m = (line_ini[2]-line_end[2])/(line_ini[0]-line_end[0])
    top_coor = corte
    right_coor = (100 - top_coor)/(m+1)
    left_coor = 100- top_coor - right_coor
    return [right_coor, top_coor, left_coor]

def streck76_QAP(*puntos):
    fig, tax = tr.figure(scale=100)
    fig.set_size_inches(10,10)
    tax.set_title("Diagrama de clasificación de rocas plutónicas (Streckeisen 1976)", pad = 50, Fontsize = 20)
    tax.gridlines(multiple=10, color = "k")
    tax.gridlines(5)
    tax.get_axes().axis('off')
    tax.horizontal_line(20)
    tax.horizontal_line(60)
    tax.horizontal_line(90)
    tax.horizontal_line(5)
    tax.ticks( multiple=10)
    tax.line([10,0],[4,60])
    tax.line([35,0],[14,60])
    tax.line([65,0],[26,60])
    tax.line([90,0],[36,60])
    tax.left_corner_label("A", Fontsize = 18 , position = (-0.02,0.05,0))
    tax.right_corner_label("P", Fontsize = 18, position=(0.97,0.05,0))
    tax.top_corner_label("Q", Fontsize = 18, offset = 0.18)
    coordenadas = [[2,95],[12.5,75],[2.5,30],
                [16,30],[35,30],[55,30],
                [65,30],[5,10],[20,10],
                [45,10],[70,10],[85,10],
                [5,2],[22,2],[50,2],
                [76,2],[91,2]]

    for indice , coordenada in enumerate(coordenadas):
        tax.annotate(str(indice+1), (coordenada[0], coordenada[1]),fontsize = 9)

    indices = '''1- Cuarzolita (Silexita) 
2- Granitoides ricos en cuarzo
3- Granito de Feldespato alcalino
4- Sieno-granito
5- Monzogranito
6- Granodiorita
7- Tonalita
8- Sienita de cuarzo
    y feldespato alcalino
9- Cuarzosienita
10- Cuarzo monzonita
11- Cuarzo monzodiorita o 
    Cuarzo monzogabro
12- Cuarzo diorita, Cuarzo gabro o
    Cuarzo anortosita
13- Sienita de feldepato
    alcalino
14- Sienita
15- Monzonita
16- Monzodiorita o Monzogabro
17- Diorita, Gabro o Anortosita'''
    tax.annotate(indices, position=(35, 100,0),
                size=9, ha='left', va='top',
                bbox=dict(boxstyle='round', fc='w'))
    for punto in puntos:
        tax.scatter([[float(punto[0]),float(punto[1])]], label = punto[2])
    fig.legend(fontsize = 10, bbox_to_anchor=(0.18,0.8 ) , bbox_transform=fig.transFigure).get_frame().set_edgecolor('k')
    file_name = "QAP_" + punto[2] + ".png"
    file_name = "QAP_general.png"
    
    #tax.show()
    tax.savefig(file_name)
    #tax.close()

def streck76_ol_2px(*puntos):
    fig, tax = tr.figure(scale=100)
    fig.set_size_inches(10,10)
    tax.set_title("Diagrama de clasificación de rocas plutónicas (Streckeisen 1976)", pad = 50, Fontsize = 20)
    tax.gridlines(multiple=10, color = "k")
    tax.gridlines(5)
    tax.get_axes().axis('off')
    tax.horizontal_line(40)
    tax.left_parallel_line(90)
    tax.horizontal_line(90)
    tax.right_parallel_line(90)
    tax.ticks( multiple=10)
    tax.line([5,90],[90,5])
    tax.line([5,5],[5,90])
    tax.line([90,5], [5,5,90])
    tax.line([65,40],[160,40], ls = 'dashed', color = 'k')
    tax.left_corner_label("Opx", Fontsize = 18, position = (-0.02,0.05,0))
    tax.right_corner_label("Cpx", Fontsize = 18,position=(0.97,0.05,0))
    tax.top_corner_label("Ol", Fontsize = 18, offset = 0.18)

    coordenadas = [[2,95],[2.5,60],[20,60],
                [37,60],[2.5,20],[40,20],
                [77,20],[3,2.5],[47,2.5],
                [93,2.5]]

    for indice , coordenada in enumerate(coordenadas):
        tax.annotate(str(indice+1), (coordenada[0], coordenada[1]),fontsize = 9)

    indices = '''1- Dunita 
2- Hazburguita
3- Lherzolita
4- Wehrlita
5- Ortopiroxenita olivínica
6- Websterita olivínica
7- Clinoperoxenita olivínica
8- Ortopiroxenita
9- Websterita
10- Clinopiroxenita'''
    tax.annotate(indices, position=(40, 100,0),
                size=10, ha='left', va='top',
                bbox=dict(boxstyle='round', fc='w'))
    for punto in puntos:
        tax.scatter([[float(punto[0]),float(punto[1])]], label = punto[2])
    fig.legend(fontsize = 10, bbox_to_anchor=(0.18,0.8 ) , bbox_transform=fig.transFigure).get_frame().set_edgecolor('k')
    tax.show()

def streck76_ol_anf_px(*puntos):
    fig, tax = tr.figure(scale=100)
    fig.set_size_inches(10,10)
    tax.set_title("Diagrama de clasificación de rocas ultramáficas (Streckeisen 1976)", pad = 50, Fontsize = 20)
    tax.gridlines(multiple=10, color = "k")
    tax.gridlines(5)
    tax.get_axes().axis('off')
    tax.horizontal_line(40)
    tax.left_parallel_line(90)
    tax.horizontal_line(90)
    tax.right_parallel_line(90)
    tax.ticks( multiple=10)
    tax.line([5,90],[90,5])
    tax.line([5,5],[5,90])
    tax.line([90,5], [5,5,90])
    tax.line(intersec([50,0],[30,40],5),[30,40])
    tax.line([65,40],[160,40], ls = 'dashed', color = 'k')
    tax.left_corner_label("Px", Fontsize = 18, position = (-0.02,0.05,0))
    tax.right_corner_label("Hbl", Fontsize = 18,position=(0.97,0.05,0))
    tax.top_corner_label("Ol", Fontsize = 18, offset = 0.18)

    coordenadas = [[2,95],[2.5,60],[20,60],
                [37,60],[2.5,20], [20,20],[60,20],
                [77,20],
                
                [3,2.5],[30,2.5],[70,2.5],
                [93,2.5]
                ]

    for indice , coordenada in enumerate(coordenadas):
        tax.annotate(str(indice+1), (coordenada[0], coordenada[1]),fontsize = 9)

    indices = '''1- Dunita 
2- Peridotita piroxénica
3- Peridoita on Hbl y Px
4- Peridotíta hornbléndica
5- Piroxenita olivínica
6- Piroxenita con Hbl y Ol
7- Hornblendita con Px y Ol
8- Hornblendita olivínica
9- Piroxenita
10- Piroxenita Hornbléndica
11- Hornblendita piroxénica
12- Hornblendita'''


    tax.annotate(indices, position=(40, 100,0),
                size=10, ha='left', va='top',
                bbox=dict(boxstyle='round', fc='w'))
    for punto in puntos:
        tax.scatter([[float(punto[0]),float(punto[1])]], label = punto[2])
    fig.legend(fontsize = 10, bbox_to_anchor=(0.18,0.8 ) , bbox_transform=fig.transFigure).get_frame().set_edgecolor('k')
    tax.show()


#***********************************
# Folk 54 y 74 para arenas

def folk_grava(*puntos):
    fig, tax = tr.figure(scale=100)
    fig.set_size_inches(10,10)
    tax.set_title("Diagrama de clasificación textural de rocas siliciclásticas (Folk 1954)", pad = 50, Fontsize = 20)
    tax.gridlines(multiple=10, color = "k")
    tax.gridlines(5)
    tax.get_axes().axis('off')
    tax.horizontal_line(5)
    tax.horizontal_line(30)
    tax.horizontal_line(80)

    tax.ticks( multiple=10)
    tax.line([50,0],[10,80])
    tax.line([10,0],[9.5,5])
    tax.line([90,0],[18,80])
    tax.left_corner_label("Lodo", Fontsize = 18, position = (-0.02,0.05,0))
    tax.right_corner_label("Arena", Fontsize = 18,position=(0.97,0.05,0))
    tax.top_corner_label("Grava", Fontsize = 18, offset = 0.18)

    coordenadas = [[4.85,90],
                [10,55],[30,55], [41.5,55],
                [20,15],[57,15],[80,15],
                [5,2], [30,2], [70,2], [93,2]
                ]

    for indice , coordenada in enumerate(coordenadas):
        tax.annotate(str(indice+1), (coordenada[0], coordenada[1]),fontsize = 9)

    indices = '''1- Conglomerado 
2- Conglomerado lodoso
3- Conglomerado
    areno-lodoso
4- Conglomerado arenoso
5- Lodolita conglomerática
6- Arenisca
    lodosa-conglomerática
7- Arenisca conglomerática
8- Lodolita
    levenente conglomerática
9- Lodolita arenosa
    levemente conglomerática
10- Arenisca lodosa
    levemente conglomerática
11- Arenisca
    levemente conglomerática'''


    tax.annotate(indices, position=(40, 100,0),
                size=10, ha='left', va='top',
                bbox=dict(boxstyle='round', fc='w'))
    for punto in puntos:
        tax.scatter([[float(punto[0]),float(punto[1])]], label = punto[2])
    fig.legend(fontsize = 10, bbox_to_anchor=(0.18,0.8 ) , bbox_transform=fig.transFigure).get_frame().set_edgecolor('k')
    tax.show()


def folk_arena_arcilla(*puntos):
    fig, tax = tr.figure(scale=100)
    fig.set_size_inches(10,10)
    tax.set_title("Diagrama de clasificación textural de rocas siliciclásticas (Folk 1954)", pad = 50, Fontsize = 20)
    tax.gridlines(multiple=10, color = "k")
    tax.gridlines(5)
    tax.get_axes().axis('off')
    tax.horizontal_line(10)
    tax.horizontal_line(50)
    tax.horizontal_line(90)

    tax.ticks( multiple=10)
    tax.line([(100/3),0], intersec([(100/3),0],[0,100],90))
    tax.line([(100/3*2),0], intersec([(100/3*2),0],[0,100],90))
    tax.left_corner_label("Arcilla", Fontsize = 18, position = (-0.02,0.05,0))
    tax.right_corner_label("Limo", Fontsize = 18,position=(0.97,0.05,0))
    tax.top_corner_label("Arena", Fontsize = 18, offset = 0.18)

    coordenadas = [[2,95],
                [5,70],[15,70], [25,70],
                [12,30],[35,30],[60,30],
                [17,5], [47,5], [80,5]
                ]

    for indice , coordenada in enumerate(coordenadas):
        tax.annotate(str(indice+1), (coordenada[0], coordenada[1]),fontsize = 9)

    indices = '''1- Arenisca
2- Arenisca arcillosa
3- Arenisca lodosa
4- Arenisca limosa
5- Arcillolita arenosa
6- Lodolita arenosa
7- Limolita arenosa
8- Arcillolita
9- Lodolita
10- Limolita'''


    tax.annotate(indices, position=(40, 100,0),
                size=10, ha='left', va='top',
                bbox=dict(boxstyle='round', fc='w'))
    for punto in puntos:
        tax.scatter([[float(punto[0]),float(punto[1])]], label = punto[2])
    fig.legend(fontsize = 10, bbox_to_anchor=(0.18,0.8 ) , bbox_transform=fig.transFigure).get_frame().set_edgecolor('k')
    tax.show()


def folk_comp(*puntos):
    fig, tax = tr.figure(scale=100)
    fig.set_size_inches(10,10)
    tax.set_title("Diagrama de clasificación composicional de rocas siliciclásticas (Folk 1974)", pad = 50, Fontsize = 20)
    tax.gridlines(multiple=10, color = "k")
    tax.gridlines(5)
    tax.get_axes().axis('off')
    tax.horizontal_line(95)
    tax.horizontal_line(75)

    tax.ticks( multiple=10)
    tax.line([(100/4),0], intersec([(100/4),0],[0,100],75))
    tax.line([(100/4*3),0], intersec([(100/4*3),0],[0,100],75))
    tax.line([50,0], intersec([50,0],[0,100],95))
    tax.left_corner_label("F", Fontsize = 18, position = (-0.02,0.05,0))
    tax.right_corner_label("L", Fontsize = 18,position=(0.97,0.05,0))
    tax.top_corner_label("Q", Fontsize = 18, offset = 0.18)

    coordenadas = [[1.1,97],
                [3,85],[11,85],
                [7,30],[25,30],[45,30],[60,30]
                ]

    for indice , coordenada in enumerate(coordenadas):
        tax.annotate(str(indice+1), (coordenada[0], coordenada[1]),fontsize = 9)

    indices = '''1- Cuarzoarenita
2- Sublitoarenita
3- Subarcosa
4- Litoarenita
5- Litoarenita Feldespática
6- Arcosa Lítica
7- Arcosa'''


    tax.annotate(indices, position=(40, 100,0),
                size=10, ha='left', va='top',
                bbox=dict(boxstyle='round', fc='w'))
    for punto in puntos:
        tax.scatter([[float(punto[0]),float(punto[1])]], label = punto[2])
    fig.legend(fontsize = 10, bbox_to_anchor=(0.18,0.8 ) , bbox_transform=fig.transFigure).get_frame().set_edgecolor('k')
    tax.show()

def folk_litic(*puntos):
    fig, tax = tr.figure(scale=100)
    fig.set_size_inches(12,12)
    tax.set_title('''Diagrama de clasificación composicional 
de rocas siliciclásticas (Folk 1974)''', pad = 50, Fontsize = 20)
    tax.gridlines(multiple=10, color = "k")
    tax.gridlines(5)
    tax.get_axes().axis('off')

    tax.ticks( multiple=10)
    tax.line([50,0],[100/3,100/3])
    tax.line([0,50],[100/3,100/3])
    tax.line([50,50],[100/3,100/3])
    tax.left_corner_label("VRF", Fontsize = 18, position = (-0.02,0.05,0))
    tax.right_corner_label("MRF", Fontsize = 18,position=(0.97,0.05,0))
    tax.top_corner_label("SRF", Fontsize = 18, offset = 0.18)

    coordenadas = [[20,60],
                [20,20],[60,20]
                ]

    for indice , coordenada in enumerate(coordenadas):
        tax.annotate(str(indice+1), (coordenada[0], coordenada[1]),fontsize = 9)

    indices = '''1- Sedarenita
2- Arenita volcánica
3- Filarenita'''


    tax.annotate(indices, position=(40, 100,0),
                size=10, ha='left', va='top',
                bbox=dict(boxstyle='round', fc='w'))
    for punto in puntos:
        tax.scatter([[float(punto[0]),float(punto[1])]], label = punto[2])
    fig.legend(fontsize = 10, bbox_to_anchor=(0.18,0.8 ) , bbox_transform=fig.transFigure).get_frame().set_edgecolor('k')
    file_name = punto[2] + ".png"
    fig.savefig(file_name)




muestras_QAP  = [[99.07,0.93,"DCF-007PA"], [71.43,28.57,"DCF-0013PA"],
                [61.23, 33.48, "DCF-0022P"], [78.01,21.99,"DCF-0025P"], [73.75, 26.25, "DCF-0049PB"], [57.8, 34.4, "DCF-0055P"],
                [53.54,33.33,"IFPS-0068PB"], [72.29,25.97,"IFPS-0026PA"],
                [83.44,15.92,"IFPS-0026PB"], [74.24, 24.45,"IFPS-0049PA"], 
                [59.61, 27.63, "IFPS-0064P"]
                ]


# streck76_QAP(*muestras_QAP)
# for muestra in muestras_QAP:
#     streck76_QAP(muestra)
