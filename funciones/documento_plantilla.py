from funciones.fijar_datos import crear_archivo
from typing import Text
from docx import Document
import pandas as pd
from docx.shared import Inches
from funciones.fotos_micro import fill_fields

def llenar_info_general():
    df = pd.read_csv('./archivos/current_interprete.csv',sep= ';',encoding= "latin")
    df2 = pd.read_csv("./archivos/current_info_muestra.csv", sep = ";", encoding= "latin")
    parametros = df2.values[-1].tolist()
    interprete = df.values[-1].tolist()
    parametros.insert(11,"")
    parametros.insert(14,interprete[0])
    parametros.insert(15,interprete[1])
    parametros = list(map(str, parametros))
    nombre_archivo = "./archivos/"+parametros[1] + ".docx"
    archivo = Document("./archivos/templates/template_1.docx")
    archivo.add_heading('INFORMACIÓN GENERAL' )
    archivo.add_paragraph()
    campos = ["IGM", "Número de campo", "Unidad litoestratigráfica", "Localidad",
              "Departamento", "Municipio", "Plancha", "Escala", "Coordenada X", 
              "Origen de Coordenadas", "Coordenada Y" ,"", "Colector", "Fecha de recolección de la muestra",
              "Analizador", "Fecha de Análisis petrográfico", "Número de puntos de conteo"]

    tabla_info_g = archivo.add_table(9,2)
    contador = 0
    for i in range(0,len(campos)//2):
        for j in range(2):
            if campos[contador] == "":
                tabla_info_g.cell(i,j%2).paragraphs[0].add_run(campos[contador]+" "+parametros[contador])
            else:
                p1 = tabla_info_g.cell(i,j%2).paragraphs[0]
                r1 = p1.add_run(campos[contador]+": ")
                r1.bold = True
                p1.add_run(parametros[contador])
            contador +=1
    tabla_info_g.cell(8,0).paragraphs[0].add_run(campos[len(campos)-1]+" "+parametros[-1])
    archivo.add_paragraph()
    archivo.save(nombre_archivo)
    return nombre_archivo

def llenar_macro(nombre_archivo):
    df2 = pd.read_csv("./archivos/current_macro.csv", sep = ";", encoding= "latin")
    campos = df2.columns.tolist()
    parametros = df2.values[-1].tolist()
    parametros = list(map(str, parametros))
    archivo = Document(nombre_archivo)
    archivo.add_heading('DESCRIPCIÓN MACROSCÓPICA' )
    # campos = ["Tipo de Roca", "Textura", "Color", "Laminación", "Bioturbación","Meteorización", "Partición",
    #             "Prueba de Fosfatos", "Reacción al HCl", "Observaciones"]

    tabla_macro = archivo.add_table(len(campos),3)
    imagen = tabla_macro.cell(0,2).merge(tabla_macro.cell(len(campos)-1,2))
    parag = imagen.paragraphs[0]
    run = parag.add_run()
    run.add_picture('archivos\Snap-91_PPL.jpg',width = Inches(1),height =Inches(1))
    for i in range(0,len(parametros)):
        for j in range(2):
            if j == 0:
                tabla_macro.cell(i,j).add_paragraph(campos[i])
            if j ==1:
                tabla_macro.cell(i,j).add_paragraph(parametros[i])

    archivo.save(nombre_archivo)


def llenar_inter_plut(nombre_archivo):
    archivo = Document(nombre_archivo)
    archivo.add_paragraph()
    archivo.add_heading("DESCRIPCIÓN MICROSCÓPICA")
    archivo.add_paragraph()
    subs = ["Textura general:", "Otras texturas o texturas especiales:", 
            "Descripción de la matriz:"]
    for i in subs:
        p1 = archivo.add_paragraph()
        r1 = p1.add_run(i)
        r1.bold = True
        r1.underline = True
        if i == subs[0]:
            p1.add_run(" Mencionar ordenada, clara y correctamente los términos texturales que indican" 
                        + "dimensión relativa de los cristales, tamaños de cristales, cristalinidad, "
                        + "relaciones mutuas entre cristales,  formas cristalinas o desarrollo relativo de caras de cristales")
        else:
            p1.add_run(" ")
        archivo.add_paragraph()
    archivo.add_page_break()
    archivo.add_paragraph()
    archivo.add_heading("COMPOSICIÓN MINERALÓGICA (% VOL) - IGM")
    archivo.add_paragraph()
    tabla_perc = archivo.add_table(12,6)
    cells = [0,1,2,3,4,4,0,2]
    content = ["MINERALES \nPRINCIPALES", "%", "MINERALES \nACCESORIOS", "%",
                "MINERALES DE ALTERACIÓN", "MINERALES DE INTRODUCCIÓN", "TOTAL", "TOTAL"]
    
    for i in range(len(cells)):
        if i >5:
            para = tabla_perc.cell(11,cells[i]).paragraphs[0]
        elif i == 5:
            para = tabla_perc.cell(6,cells[i]).paragraphs[0]
        else:
            para = tabla_perc.cell(0,cells[i]).paragraphs[0]
        r1 = para.add_run(content[i])
        r1.bold = True
        r1.underline = True
    tabla_perc.cell(0,4).merge(tabla_perc.cell(0,5))
    tabla_perc.cell(6,4).merge(tabla_perc.cell(6,5))
       
    archivo.add_paragraph()
    clas_roc = archivo.add_paragraph()
    run = clas_roc.add_run("CLASIFICACIÓN DE LA ROCA ")
    run.bold = True
    run.underline = True
    r2 = clas_roc.add_run("(Basada en Streckeisen, 1976):")
    r2.underline = True
    clas_roc.add_run(" La clasificación")
    archivo.add_paragraph()
    archivo.add_heading("DESCRIPCIÓN MICROSCÓPICA DE MINERALES")
    archivo.add_paragraph()
    p1 = archivo.add_paragraph()
    r1 = p1.add_run("Mineral 1:")
    r1.bold = True
    r1.underline = True
    p1.add_run(" Descripción concisa y completa de rasgos generales y particulares," 
                + "sin olvidar tamaño, forma, color, distribución, relaciones texturales, "
                + "extinción, clivaje, etc")
    archivo.add_paragraph()
    archivo.add_heading("OBSERVACIONES")
    archivo.add_paragraph()
    archivo.save(nombre_archivo)

def llenar_inter_dinamico(nombre_archivo):
    archivo = Document(nombre_archivo)
    archivo.add_paragraph()
    archivo.add_heading("DESCRIPCIÓN MICROSCÓPICA")
    archivo.add_paragraph()
    
def llenar_inter_silici(nombre_archivo):
    archivo = Document(nombre_archivo)
    archivo.add_page_break()
    archivo.add_paragraph()
    archivo.add_heading("DESCRIPCIÓN MICROSCÓPICA" + '_' + 'Colocar IGM')
    archivo.add_paragraph()
    archivo.add_heading("DESCRIPCIÓN TEXTURAL",2)
    archivo.add_paragraph()
    lista= ['HOMOGENEIDAD DE LA ROCA:','TAMAÑO DE GRANO PROMEDIO:',
            'RANGO DE TAMAÑOS:','SELECCIÓN:','REDONDEZ PROMEDIO:',
            'ESFERICIDAD PROMEDIO:', 'MADUREZ TEXTURAL:']
    for i in lista:
        p1= archivo.add_paragraph()
        r1= p1.add_run(i)
        r1.italic = True
        r1.bold = True
        p1.add_run(" ")
    p1 = archivo.add_paragraph()
    list= ['GRAVA ______ (%)','Tamaño promedio:  ____	 Redondez:  _____ Esfericidad:  ______', 'ARENA _____(%)', 
           'Tamaño promedio:  ____	 Redondez:  _____ Esfericidad:  ______', 'LODO ________(%)',
           'Arcilla__________% Tamaño promedio fracción arcilla:______mm/μm\nLimo __________% Tamaño promedio fracción limo:______mm/μm',
           'CONTACTO ENTRE GRANOS:', 'Flotante:______% Tangencial:______%\nLongitudinal:______% Cóncavo-convexo:______%\nSuturado:______%',
           'SOPORTE DE LA ROCA:', 'Granos terrígenos-aloquímicos_________% Minerales arcillosos_________%' ]
    
    contador = 0
    for i in list: #los datos de grava y tamaño y lo demás de la list se pueden llenar con info de interfaz
        if contador %2 == 0:
            p1= archivo.add_paragraph()
            r1= p1.add_run(i)
            r1.italic = True
            r1.bold = True
            p1.add_run(" ")
        else:
            p1= archivo.add_paragraph()
            r1= p1.add_run(i)
            p1.add_run(" ")
        archivo.add_paragraph()    
        contador = contador +1 
    p1 = archivo.add_paragraph()
    r1 = p1.add_run("POROSIDAD:") 
    r1.bold = True
    r1.underline = True
    p1.add_run('_______% Primaria:_______% Secundaria:_______% \nTipo(s), origen y descripción')
    archivo.add_paragraph()
    r1 = p1.add_run("ESTRUCTURAS:") 
    r1.bold = True
    r1.underline = True
    
    archivo.add_paragraph()
    archivo.add_heading('CLASIFICACIÓN TEXTURAL')
    archivo.add_paragraph()
    clas_roc = archivo.add_paragraph()
    run = clas_roc.add_run("NOMBRE TEXTURAL ")
    run.bold = True
    run.underline = True
    r2 = clas_roc.add_run("(Folk, 1954):")
    r2.underline = True
    archivo.add_paragraph('(Grava + Arena + Lodo = 100%)')
    archivo.add_page_break()
    archivo.save(nombre_archivo)    


def llenar_inter_regional(nombre_archivo):
    archivo = Document(nombre_archivo)
    archivo.add_paragraph()
    archivo.add_heading("DESCRIPCIÓN MICROSCÓPICA")
    archivo.add_paragraph()
    subs = ["Textura general:", "Otras texturas:", "Observaciones:"]
    for i in subs:
        p1 = archivo.add_paragraph()
        r1 = p1.add_run(i)
        r1.bold = True
        r1.underline = True
        p1.add_run(" ")
        archivo.add_paragraph()

    archivo.add_page_break()
    archivo.add_paragraph()
    archivo.add_heading("COMPOSICIÓN MINERALÓGICA (%Vol) - ")
    archivo.add_paragraph()
    tabla_perc = archivo.add_table(12,6)
    cells = [0,1,2,3,4,4,0,2]
    content = ["MINERALES \nPRINCIPALES", "%", "MINERALES \nACCESORIOS", "%",
                "MINERALES DE ALTERACIÓN", "MINERALES DE INTRODUCCIÓN", "TOTAL", "TOTAL"]
    
    for i in range(len(cells)):
        if i >5:
            para = tabla_perc.cell(11,cells[i]).paragraphs[0]
        elif i == 5:
            para = tabla_perc.cell(6,cells[i]).paragraphs[0]
        else:
            para = tabla_perc.cell(0,cells[i]).paragraphs[0]
        r1 = para.add_run(content[i])
        r1.bold = True
        r1.underline = True
    tabla_perc.cell(0,4).merge(tabla_perc.cell(0,5))
    tabla_perc.cell(6,4).merge(tabla_perc.cell(6,5))
    archivo.add_paragraph()
    caracteristicas = ["PARAGÉNESIS:", "TIPO DE METAMORFÍSMO:",
                       "FACIES DE METAMORFISMO:", "PROTOLITO:"]
    for i in caracteristicas:
        p1 = archivo.add_paragraph()
        r1 = p1.add_run(i)
        r1.bold = True
        r1.underline = True
        p1.add_run(" ")

    clas_roc = archivo.add_paragraph()
    run = clas_roc.add_run("CLASIFICACIÓN DE LA ROCA ")
    run.bold = True
    run.underline = True
    r2 = clas_roc.add_run("(Basada en SSMR, 2007):")
    r2.underline = True
    clas_roc.add_run(" La clasificación")
    archivo.add_paragraph()
    archivo.add_heading("DESCRIPCIÓN MICROSCÓPICA DE MINERALES")
    archivo.add_paragraph()
    p1 = archivo.add_paragraph()
    r1 = p1.add_run("Mineral 1:")
    r1.bold = True
    r1.underline = True
    p1.add_run(" Descripción concisa y completa de rasgos generales y particulares, "
                + "sin olvidar tamaño, forma, color, distribución, relaciones texturales, "
                + "extinción, clivaje, etc")
    archivo.add_paragraph()
    archivo.save(nombre_archivo)

def llenar_des_micro(nombre_archivo):
    asdf = 1

def llenar_fotos_micro(nombre_archivo):
    archivo = Document(nombre_archivo)
    archivo.add_page_break()
    archivo.add_paragraph()
    archivo.add_heading("REGISTRO FOTOGRÁFICO")
    archivo.add_paragraph()
    url_img1= 'archivos\Snap-91_PPL.jpg'
    url_img2= 'archivos\Snap-92.jpg'

    text = 'Habia una vez una iguana tomando cafe '
        
    archivo = fill_fields(archivo,url_img1,url_img2,text)
    archivo.save(nombre_archivo)


# archivo = Document()
# tabla_macro = archivo.add_table(10,3)
# imagen = tabla_macro.cell(0,2).merge(tabla_macro.cell(8,2))
# parag = imagen.paragraphs[0]
# run = parag.add_run()
# run.add_picture('archivos\Snap-91_PPL.jpg',width = Inches(1),height =Inches(1))
# archivo.add_paragraph("ñandú")
# archivo.save("prueb.docx") 
# nombre_a = "./archivos/perritos.docx"
# llenar_info_general( nombre_a, "IGM:", "Número de campo", "Unidad litoestratigráfica", "Localidad",
#               "Departamento", "Municipio", "Plancha", "Escala", "Coordenada X:", 
#               "Origen de Coordenadas:", "Coordenada Y:" ,"", "Colector", "Fecha de recolección de la muestra",
#               "Analizador", "Fecha de Análisis petrográfico", "Número de puntos de conteo")

