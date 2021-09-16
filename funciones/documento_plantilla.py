from typing import Text
from docx import Document
import pandas as pd
from docx.shared import Inches
#from funciones.fotos_micro import fill_fields
from PyQt5.QtWidgets import QFileDialog

def fill_fields(archivo, url_img1,url_img2,text):
    # create the table 
    table = archivo.add_table(2,2)
    
    # merge second table
    A = table.cell(1,0).merge(table.cell(1,1))
    
    # add first image
    paragraph = table.cell(0,0).paragraphs[0]
    run = paragraph.add_run()
    run.add_picture(url_img1,width = Inches(2.95),height =Inches(2.18) )
    
    # add second image
    paragraph = table.cell(0,1).paragraphs[0]
    run = paragraph.add_run()
    run.add_picture(url_img2,width = Inches(2.95) ,height =Inches(2.18) )
    
    # add descripction
    A.add_paragraph(text)
    return archivo

def llenar_info_general():
    df = pd.read_csv('./archivos/current_general.csv',sep= ';',encoding= "latin")
    name = str(df["numero_campo"][0])
    nombre_archivo = QFileDialog.getSaveFileName(directory= name,filter= "documents (*.docx *.doc)")[0]
    parametros = df.iloc[0].tolist()
    parametros.pop()
    parametros.pop()
    parametros.insert(11,"")
    parametros = list(map(str, parametros))
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
    general = pd.read_csv("./archivos/current_general.csv", sep = ";", encoding= "latin")
    if general["Tipo_r"][0] != "Sedimentaria":
        df = pd.read_csv("./archivos/current_macro.csv", sep = ";", encoding= "latin")
    else:
        df = pd.read_csv("./archivos/current_macro_sed.csv", sep = ";", encoding= "latin")
    campos = df.columns.tolist()
    parametros = df.values[-1].tolist()
    parametros = list(map(str, parametros))
    archivo = Document(nombre_archivo)
    archivo.add_heading('DESCRIPCIÓN MACROSCÓPICA' )
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
    archivo.add_heading('ASPECTOS TEXTURALES',2)
    archivo.add_paragraph()
    archivo.add_heading('DESCRIPCIÓN DE MICROESTRUCTURAS: ',3)
    archivo.add_paragraph()
    archivo.add_heading('FABRICA: ',3)
    list=['Cohesión _____','Foliación_____','Tamaño de porfiroclastos _____ (µ)'
    'Proporción de matriz____%','Recristalización_____']
    for i in list:
        p1= archivo.add_paragraph(i)
        p1.add_run(" ")
    archivo.add_paragraph()
    archivo.add_heading('TIPO DE DEFORMACIÓN:',3)
    archivo.add_paragraph('Frágil _____')
    archivo.add_paragraph('Dúctil_____  Grado: Bajo	_____Medio_____Alto_____')
    archivo.add_paragraph()
    archivo.add_heading('ASPECTOS COMPOSICIONALES___ IGM',2)
    archivo.add_paragraph()
    tabla_comp_din= archivo.add_table(10,10)
    cells = [0,1,2,3,4,4,0,2]
    content = ["PORFIROCLASTOS", "%", "MINERALES \nACCESORIOS", "%",
                "MINERALES DE ALTERACIÓN", "MINERALES DE INTRODUCCIÓN", "TOTAL", "TOTAL"]
    
    for i in range(len(cells)):
        if i >5:
            para = tabla_comp_din.cell(1,cells[i]).paragraphs[0]
        elif i == 5:
            para = tabla_comp_din.cell(6,cells[i]).paragraphs[0]
        else:
            para = tabla_comp_din.cell(0,cells[i]).paragraphs[0]
        r1 = para.add_run(content[i])
        r1.bold = True
        r1.underline = True
    tabla_comp_din.cell(0,0).merge(tabla_comp_din.cell(3,0))
    tabla_comp_din.cell(0,1).merge(tabla_comp_din.cell(3,1))
    tabla_comp_din.cell(0,2).merge(tabla_comp_din.cell(0,5))
    tabla_comp_din.cell(0,6).merge(tabla_comp_din.cell(0,9))
    


    archivo.save(nombre_archivo)  
    
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
    archivo.add_paragraph()
    archivo.add_heading("DESCRIPCIÓN COMPOSICIONAL" + '_' + 'Colocar IGM')
    archivo.add_paragraph()
    archivo.add_heading("TERRIGENOS" + '___'+ '(%)',3)
    archivo.add_paragraph()
    list2= ['Cuarzo _____ (%)','Monocristalino:______(%) Tamaño promedio:___mm/μm Esfericidad:___Redondez:___'
            '\nPolicristalino:_____%	Tamaño promedio:____mm/μm Esfericidad____Redondez:___'
            '\nObservaciones:____ ','Chert:___%', 'Tamaño promedio: mm/μm Esfericidad_____ Redondez:_____', 'Feldespato: %',
            'Potásico:_____% Tamaño promedio:_____mm/μm	Esfericidad	_____Redondez:_____'	
            '\nSódico-Cálcico	_____% Tamaño promedio:_____mm/μm Esfericidad_____Redondez:_____']
    contador=0
    for i in list2: #los datos de grava y tamaño y lo demás de la list se pueden llenar con info de interfaz
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
    list3=[ 'Micas____%','Descripción ______','Minerales Arcillosos______%',' Descripción_____',
            'Granos Aloquímicos	_____%','Descripción_____', 'Otros Terrígenos_____%','Descripción_____',
            'Opacos_____%','Descripción_______']       
    contador=0
    for i in list3: #los datos de grava y tamaño y lo demás de la list se pueden llenar con info de interfaz
        if contador %2 == 0:
            p1= archivo.add_paragraph(False)
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
    archivo.add_paragraph()
    archivo.add_heading('LÍTICOS (Ígneos, Metamórficos, Sedimentarios) ______ (%)',3)
    archivo.add_paragraph()
    list4= ['Líticos Metamórficos: 		%',	
            'Tamaño promedio:_____mm/μm	Esfericidad:_____Redondez:_____',	
            'Líticos Volcánicos:_____%',	
            'Tamaño promedio:_____mm/μm	Esfericidad:_____Redondez:_____',	
            'Líticos Plutónicos:_____%',	
            'Tamaño promedio:_____mm/μm	Esfericidad:_____Redondez:_____',	
            'Líticos Sedimentarios:_____%',
            'Tamaño promedio:_____mm/μm	Esfericidad:_____Redondez:_____'	
            '\nObservaciones:_____', 'Materia Orgánica_____%', 'Tipo(s):_____',
            'Cemento:_____%','Tipo(s):''\nTamaño cristalino_____mm/μm', 'Otros Ortoquímicos:_____%',	
            'Tipo(s)(incluye minerales autigénicos):_____' '\nTamaño:____mm/μm']
    contador=0
    for i in list4: 
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
    archivo.add_paragraph()
    archivo.add_heading('CLASIFICACIÓN COMPOSICIONAL')
    archivo.add_paragraph()
    clas_roc = archivo.add_paragraph()
    run = clas_roc.add_run("NOMBRE COMPOSICIONAL ")
    run.bold = True
    run.underline = True
    r2 = clas_roc.add_run("(Folk, 1954):")
    r2.underline = True
    archivo.add_paragraph()
    archivo.add_heading('DIAGÉNESIS',2)
    z1=archivo.add_paragraph('Autigénesis:')
    z2=archivo.add_paragraph('Recristalización:')
    z1.bold= True
    z2.bold= True

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

