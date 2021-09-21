# Configuacion de entorno 
from pandas.core import base
from interfaz_grafica.interfaz_de_usuario import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap
from funciones.documento_plantilla import *
from funciones.fijar_datos import *
from PyQt5.QtWidgets import QMessageBox

import sys


class interfaz(Ui_MainWindow):
    def __init__( self ):
        super().__init__()

    
    def setupUi( self, MW ):
        super().setupUi( MW )
        crear_los_archivos()
        #Inicialización de las cajas de conteo
        self.initial_box()
        self.contar_puntos(55)

        # botones e input del tab general
        self.boton_guardar_calibracion.clicked.connect(self.calibracion_escala)
        self.boton_guardar_tipo_roca.clicked.connect(self.guardar_tipo_roca) 
        self.input_tipo_roca.currentTextChanged.connect(self.actualizar_despliegue)
        self.boton_agregar_mineral.clicked.connect(self.click_agregar)
        # self.boton_ver_lista.clicked.connect(self.lista_nueva)
        self.boton_guardar_interprete.clicked.connect(self.interprete)
        self.boton_guardar_info_muestra.clicked.connect(self.info_muetra)

        #tab macro
        self.boton_cargar_foto.clicked.connect(self.cargar_foto_macro)
        self.boton_cargar_escala.clicked.connect(self.cargar_escala)
        self.boton_guardar_macro.clicked.connect(self.guardar_macro)

        # botones tab conteo
        self.boton_cal_siguiente_p.clicked.connect(self.siguiente_calc)
        self.boton_sil_siguiente_p.clicked.connect(self.siguiente_silici)
        self.boton_plut_siguiente_p.clicked.connect(self.siguiente_pluton)
        self.boton_vol_siguiente_p.clicked.connect(self.siguiente_volcanica)
        self.boton_vol_clas_siguiente_p.clicked.connect(self.siguiente_vol_clas)
        self.boton_reg_siguiente_p.clicked.connect(self.siguiente_regional)
        self.boton_din_siguiente_p.clicked.connect(self.siguiente_dinamico)

        # Observaciones sedimentarias y metamorficas
        self.boton_guardar_observaciones_gen.clicked.connect(self.observaciones)
        # observaciones igneas
        self.boton_guardar_observaciones_gen_ig.clicked.connect(self.observaciones_ig)
        # descripciones micro
        self.boton_siguiente_desc_micro.clicked.connect(self.guardar_descripcion_micro)
        self.boton_cargar_ppl.clicked.connect(self.cargar_ppl)
        self.boton_cargar_xpl.clicked.connect(self.cargar_xpl)

        #exportaciones
        self.boton_exp_csv.clicked.connect(self.export_csv)
        self.boton_exp_histograma.clicked.connect(self.export_histograma)
        self.boton_exp_formato.clicked.connect(self.export_formato)
        self.boton_exp_triangulo.clicked.connect(self.export_triangulo)
        

# tab general

    # calibración medidas
#-------------------------------------------------------------------------------
    def calibracion_escala(self):
        '''
        Guardo los parametros de calibracion de objetivos del microscopio en el
        archivo calibracion_escala.csv
        '''
        reticulas = self.input_reticulas.value()
        reticulas = str(reticulas)
        milimetros = self.input_milimetros.value()
        milimetros = str(milimetros)
        objetivo = self.input_objetivo.value()
        objetivo = str(objetivo)

        if (int(reticulas) != 0 and int(milimetros) != 0):
            data = {"reticulas": [reticulas],
                    "milimetros": [milimetros],
                    "objetivo": [objetivo]}
            llenado_csv("calibracion_escala", data)
        else :
            self.funcion_error_msg("Entrada invalida","Error de entrada",
                                "Se ingreso milimetros o reticulas en cero")

#-------------------------------------------------------------------------------
    def funcion_error_msg(self,texto,error,detalles):
        '''
        Funcion encargada de desplegar mensajes de error personalizados
        '''
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(texto)
        msg.setWindowTitle(error)
        msg.setDetailedText(detalles)
        msg.exec_()

#-------------------------------------------------------------------------------
    def click_agregar(self):
        '''
        Guarda la combinacion simbolo mineral en el archivo temporal 
        Diccionario_simbolos.csv
        '''
        
        simbolo = self.input_simbolo.text()
        mineral = self.input_mineral_config.text()
        if not validar_exitencia_archivo("./archivos/Diccionario_simbolos.csv"):
            Crear_Archivo("Diccionario_simbolos")
        if agregar_elemento(simbolo, mineral):
            self.input_simbolo.clear()
            self.input_mineral_config.clear()
            self.label_error.setText ('El mineral fue agregado exitosamente')
        elif simbolo == "":
            self.funcion_error_msg("Casilla Vacia","Error de entrada", "")
        else:
            self.funcion_error_msg("'El mineral ya existe'","Error de entrada","")
            
#-------------------------------------------------------------------------------
    def info_muetra(self):
        '''
        Funcion que recopila la informacion contenida en el panel de informacion
        de la muestra, y guarda la informacion en un archivo temporal llamado
        current_general.csv 
        '''
        
        igm = self.input_igm.text() # igm : indice general de muestra
        numero_campo= self.input_n_campo.text()
        unidad_lito= self.input_unidad_lito.text()
        departamento= self.input_departamento.text()
        localidad= self.input_localidad.text()
        municipio= self.input_municipio.text()
        plancha= self.input_plancha.text()
        escala= self.input_escala.text()
        origen_coor= self.input_origen.text()
        coor_x= self.input_coor_x.text()
        colector= self.input_colector.text()
        coor_y= self.input_coor_y.text()
        fecha_recol= self.input_fecha_recolec.text()
        cantidad_p= self.input_cantidad_puntos.text()

        data = {"igm": [igm],"numero_campo": [numero_campo],
                "unidad_lito": unidad_lito,"localidad": [localidad],
                "departamento": [departamento], "municipio": [municipio],
                "plancha" : [plancha], "escala" : [escala],
                "coor_x":[coor_x], "origen_coor" : [origen_coor],
                "coor_y": [coor_y],"colector": [colector], 
                "fecha_recol": [fecha_recol], "cantidad_p": [cantidad_p]}

        llenado_csv("current_general",data)

        #self.input_cantidad_puntos.clear()
        #self.input_fecha_recolec.clear()
        #self.input_igm.clear()
        #self.input_n_campo.clear()
        #self.input_unidad_lito.clear()
        #self.input_localidad.clear()
        #self.input_departamento.clear()
        #self.input_municipio.clear()
        #self.input_plancha.clear()
        #self.input_escala.clear()
        #self.input_origen.clear()
        #self.input_coor_x.clear()
        #self.input_coor_y.clear()
        #self.input_colector.clear()
    
#-------------------------------------------------------------------------------
    def actualizar_despliegue(self):
        '''
        Cuando se selecciona un tipo de roca esta funcion permite la seleccion
        automatica del subtipo dado 
        '''

        self.input_subtipo_roca.clear()
        if self.input_tipo_roca.currentText() == "Sedimentaria":
            list = ["Siliciclástica", "Calcárea"]
            for i in list:
                self.input_subtipo_roca.addItem(i)
        elif self.input_tipo_roca.currentText() == "Ígnea":
            list = ["Plutónica", "Volcánica", "Volcanoclástica"]
            for i in list:
                self.input_subtipo_roca.addItem(i)
        elif self.input_tipo_roca.currentText() == "Metamórfica":
            list = ["Dinámico", "Regional o de Contacto"]
            for i in list:
                self.input_subtipo_roca.addItem(i) 

    # def lista_nueva(self):
    #     a = None
    #     Crear_Archivo("./archivos/lista_simbolos_minerales.csv", ['Simbolo', 'Mineral' ])

#-------------------------------------------------------------------------------
    def interprete(self):
        '''
        Guarda el nombre y fecha de interpretacion en el archivo temporal 
        current_general.csv
        '''
        nombre = self.input_nombre_interprete.text()
        fecha = self.input_fecha_analisis.text()

        data = {"Intemprete": [nombre] , "Fecha_interp": [fecha]}
        llenado_csv("current_general",data)
        self.guardar_tipo_roca()

#-------------------------------------------------------------------------------
    def guardar_tipo_roca(self):
        '''
        Guarda el tipo y subtipo de roca en el archivo temporal
        current_general.csv
        '''

        subtipo_r = self.input_subtipo_roca.currentText()
        tipo_r = self.input_tipo_roca.currentText()
        
        # A partir de la seleccion de tipo y subtipo se actualizan los campos 
        # desplegados (mostrados) en la pestaña 2 y 3

        if subtipo_r == "Siliciclástica":
            self.hide_boxes()
            self.frame_siliciclastica.setVisible(True)
            self.frame_descripcion_macro_sed.setVisible(True)
        elif subtipo_r == "Calcárea":
            self.hide_boxes()
            self.frame_calcarea.setVisible(True)
            self.frame_descripcion_macro_sed.setVisible(True)
        elif subtipo_r == "Plutónica":
            self.hide_boxes()
            self.frame_pluton.setVisible(True)
            self.frame_descripcion_macro_ot.setVisible(True)
        elif subtipo_r == "Volcánica":
            self.hide_boxes()
            self.frame_volcanica.setVisible(True)
            self.frame_descripcion_macro_ot.setVisible(True)
        elif subtipo_r == "Volcanoclástica":
            self.hide_boxes()
            self.frame_volcanoclastica.setVisible(True)
            self.frame_descripcion_macro_ot.setVisible(True)
        elif subtipo_r == "Regional o de Contacto":
            self.hide_boxes()
            self.frame_regional.setVisible(True)
            self.frame_descripcion_macro_ot.setVisible(True)
        else: # subTpo dinamico
            self.hide_boxes()
            self.frame_dinamico.setVisible(True)
            self.frame_descripcion_macro_ot.setVisible(True)

        data = {"Tipo_r": [tipo_r],"Subt_r": [subtipo_r]}
        llenado_csv("current_general", data)

    #tab marco
#-------------------------------------------------------------------------------
    def cargar_foto_macro(self):
        ''' 
        se encarga de realizar la lectura de las rutas de los archivos para 
        posteriormente mostralor en la interfaz grafica 
        '''

        ruta, foto = agregar_imagen()
        self.label_foto_macro.setPixmap(foto)
        data = {"url_foto": [ruta]}

        general = pd.read_csv("./archivos/current_general.csv",
                               sep = ";", encoding= "latin")

        if general["Tipo_r"][0] != "Sedimentaria":
            llenado_csv("current_macro", data)
        else:
            llenado_csv("current_macro_sed", data)

#-------------------------------------------------------------------------------
    def contar_puntos(self,numero):
        '''
        configura ( setea ) el numero dentro del lcd display
        '''
        self.output_contador.setProperty('value',numero)

#-------------------------------------------------------------------------------
    def cargar_escala(self):
        '''
        Colocar descripcion
        '''
        ruta, foto = agregar_imagen()
        self.label_escala_macro.setPixmap(foto)
        data = {"url_escala": [ruta]}
        general = pd.read_csv("./archivos/current_general.csv", 
                              sep = ";", encoding= "latin")
        if general["Tipo_r"][0] != "Sedimentaria":
            llenado_csv("current_macro", data)
        else:
            llenado_csv("current_macro_sed", data)
        

    def guardar_macro(self):
        if self.frame_descripcion_macro_sed.isVisible() == True:
            tipo_r = (self.input_mac_tipo_roca.text())
            textura = (self.input_mac_textura.text())
            color = (self.input_mac_color.text())
            laminacion = (self.input_mac_laminacion.text())
            bioturbacion= (self.input_mac_bioturb.text())
            meteorizacion= (self.input_mac_meteor.text())
            particion = (self.input_mac_particion.text())
            fosfatos = self.input_mac_fosfatos.text()
            hcl = self.input_mac_hcl.text()
            observaciones = self.input_mac_obs_sed.toPlainText().replace("\n"," ")
            campos = ["tipo_roca", "textura", "color", "laminación", "bioturbacion",
                        "meteorizacion", "particion", "prueba_fosfatos", "pureba_HCl", "observaciones"]
            parametros = [[tipo_r], [textura], [color], [laminacion], [bioturbacion], [meteorizacion],
                            [particion], [fosfatos], [hcl], [observaciones]]
            data = dict(zip(campos,parametros))
            llenado_csv("current_macro_sed", data)
        else:
            observaciones = self.input_mac_obs_ot.toPlainText().replace("\n"," ")
            data = {"observaciones" : [observaciones]}
            llenado_csv("current_macro", data)

        # self.input_mac_tipo_roca.clear()
        # self.input_mac_textura.clear()
        # self.input_mac_color.clear()
        # self.input_mac_laminacion.clear()
        # self.input_mac_bioturb.clear()
        # self.input_mac_meteor.clear()
        # self.input_mac_particion.clear()
          
# tab conteo
    def initial_box(self):

        self.hide_boxes()

        # tamaño volcanica
        self.frame_volcanica.setGeometry(QtCore.QRect(20,20,451,511))
        self.layout_volcanica.setGeometry(QtCore.QRect(0,0,431,451))
        self.titulo_volcanica.setGeometry(QtCore.QRect(0,0,451,31))

        # tamaño volcanoclastica
        self.frame_volcanoclastica.setGeometry(QtCore.QRect(20,20,451,511))
        self.layout_volcanoclastica.setGeometry(QtCore.QRect(0,0,431,451))
        self.titulo_volcanoclastica.setGeometry(QtCore.QRect(0,0,451,31))

        # tamaño regional
        self.frame_regional.setGeometry(QtCore.QRect(20,20,451,511))
        self.layout_regional.setGeometry(QtCore.QRect(0,0,431,451))
        self.titulo_regional.setGeometry(QtCore.QRect(0,0,451,31))

        # tamaño dinamico
        self.frame_dinamico.setGeometry(QtCore.QRect(20,20,451,511))
        self.layout_dinamico.setGeometry(QtCore.QRect(0,0,431,451))
        self.titulo_dinamico.setGeometry(QtCore.QRect(0,0,451,31))

        # tamaño calcarea
        self.frame_calcarea.setGeometry(QtCore.QRect(20,20,451,511))
        self.layout_calcarea.setGeometry(QtCore.QRect(0,0,431,451))
        self.titulo_calcarea.setGeometry(QtCore.QRect(0,0,451,31))
        # tamaño siliciclastica
        self.frame_siliciclastica.setGeometry(QtCore.QRect(20,20,451,511))
        self.layout_siliciclastica.setGeometry(QtCore.QRect(0,0,431,451))
        self.titulo_siliciclastica.setGeometry(QtCore.QRect(0,0,451,31))
        # tamaño pluton
        self.frame_pluton.setGeometry(QtCore.QRect(20,20,451,511))
        self.layout_pluton.setGeometry(QtCore.QRect(0,0,431,451))
        self.titulo_pluton.setGeometry(QtCore.QRect(0,0,451,31))
        
        #tamaño observaciones sedimentarias y metamorficas
        self.frame_observaciones.setVisible(False)
        self.frame_observaciones.setGeometry(QtCore.QRect(480,20,431,301))
        self.titulo_observaciones.setGeometry(QtCore.QRect(10,0,431,31))
        self.layout_observaciones.setGeometry(QtCore.QRect(0,0,431,301))

        #tamaño observaciones igneas
        self.frame_observaciones_ig.setGeometry(QtCore.QRect(480,20,431,301))
        self.titulo_observaciones_ig.setGeometry(QtCore.QRect(10,0,431,31))
        self.layout_observaciones_ig.setGeometry(QtCore.QRect(0,0,431,301))

        #self.frame_observaciones_ig.setVisible(False)
        self.frame_observaciones_ig.setGeometry(QtCore.QRect(480,20,431,301))
        self.titulo_observaciones_ig.setGeometry(QtCore.QRect(10,0,431,31))
        self.layout_observaciones_ig.setGeometry(QtCore.QRect(0,0,431,301))

        #tab macro
        self.frame_descripcion_macro_sed.setGeometry(QtCore.QRect(20,20,461,471))
        self.frame_descripcion_macro_ot.setGeometry(QtCore.QRect(20,20,461,471))
        

    def hide_boxes(self):
        self.frame_siliciclastica.setVisible(False)
        self.frame_calcarea.setVisible(False)
        self.frame_pluton.setVisible(False)
        self.frame_volcanica.setVisible(False)
        self.frame_volcanoclastica.setVisible(False)
        self.frame_regional.setVisible(False)
        self.frame_dinamico.setVisible(False)
        self.frame_descripcion_macro_ot.setVisible(False)
        self.frame_descripcion_macro_sed.setVisible(False)

    # funcion dinamico
    def siguiente_dinamico(self):
        archivo = "Conteo_dinamicas"
        mineral= [(self.input_din_mineral.text())]
        tipo= [(self.input_din_tipo.currentText())]
        size= [(self.input_din_size.value())]
        forma= [(self.input_din_forma.currentText())]
        borde= [(self.input_din_borde.currentText())]
        geometria= [(self.input_din_geometria.currentText())]
        observaciones= [(self.input_din_observa.toPlainText())]
        parametros = [mineral, tipo, size, forma, borde, geometria, observaciones]
        if agregar_puntos(archivo, parametros):
            self.input_din_mineral.clear()
            self.input_din_tipo.setCurrentText("Porfiroclásto")
            self.input_din_size.setValue(0)
            self.input_din_forma.setCurrentText("Ideoblástico")
            self.input_din_borde.setCurrentText("Recto")
            self.input_din_geometria.setCurrentText("Poligonal")
            self.input_din_observa.clear()
        else:
            print("Simbolo incorrecto")

    # funcion regional
    def siguiente_regional(self):
        archivo = "Conteo_regionales"
        mineral= [(self.input_reg_mineral.text())]
        size= [(self.input_reg_size.value())]
        forma= [(self.input_reg_forma.currentText())]
        borde= [(self.input_reg_borde.currentText())]
        geometria= [(self.input_reg_geometria.currentText())]
        observaciones= [(self.input_reg_observa.toPlainText())]
        parametros = [mineral, size, forma, borde, geometria, observaciones]
        if agregar_puntos(archivo, parametros):
            self.input_reg_mineral.clear()
            self.input_reg_size.setValue(0)
            self.input_reg_forma.setCurrentText("Ideoblástico")
            self.input_reg_borde.setCurrentText("Recto")
            self.input_reg_geometria.setCurrentText("Poligonal")
            self.input_reg_observa.clear()
        else:
            print("Simbolo incorrecto")
    # funcion volcanoclastica
    def siguiente_vol_clas(self):
        archivo = "Conteo_volcanoclasticas"
        mineral = [(self.input_vol_clas_mineral.text())]
        size= [(self.input_vol_clas_size.value())]
        redondez= [(self.input_vol_clas_redond.currentText())]
        esfericidad= [(self.input_vol_clas_esfer.currentText())]
        t_contacto= [(self.input_vol_clas_contacto.currentText())]
        t_fragmento= [(self.input_vol_clas_tipo_frag.currentText())]
        observaciones= [(self.input_vol_clas_observa.toPlainText())]
        parametros = [mineral, size, redondez, esfericidad, t_contacto, t_fragmento, observaciones]
        if agregar_puntos(archivo, parametros):
            self.input_vol_clas_mineral.clear()
            self.input_vol_clas_size.setValue(0)
            self.input_vol_clas_redond.setCurrentText("Angular")
            self.input_vol_clas_esfer.setCurrentText("Elongado")
            self.input_vol_clas_contacto.setCurrentText("Tangencial")
            self.input_vol_clas_tipo_frag.setCurrentText("Cristales y fragmentos cristalinos")
            self.input_vol_clas_observa.clear()
        else:
            print("Simbolo incorrecto")

    # funcion volcanica
    def siguiente_volcanica(self):
        archivo = "Conteo_volcanicas"
        mineral= [(self.input_vol_mineral.text())]
        size= [(self.input_vol_size.value())]
        forma= [(self.input_vol_forma.currentText())]
        observaciones= [(self.input_vol_observa.toPlainText())]
        parametros = [mineral, size, forma, observaciones]
        if agregar_puntos(archivo, parametros):
            self.input_vol_mineral.clear()
            self.input_vol_size.clear()
            self.input_vol_forma.setCurrentText("Euhedral")
            self.input_vol_observa.clear()
        else:
            print("Simbolo incorrecto")
    #funcion plutonico
    def siguiente_pluton(self):
        archivo = "Conteo_plutonicas"
        mineral=[(self.input_plut_mineral.text())]
        size=[(self.input_plut_size.value())]
        forma=[(self.input_plut_forma.currentText())]
        genesis=[(self.input_plut_gene.currentText())]
        observaciones=[(self.input_plut_observa.toPlainText())]
        parametros = [mineral, size, forma, genesis, observaciones]
        if agregar_puntos(archivo, parametros):

            self.input_plut_mineral.clear()
            self.input_plut_size.setValue(0)
            self.input_plut_forma.setCurrentText("Euhedral")
            self.input_plut_gene.setCurrentText("Primario")
            self.input_plut_observa.clear()
        else:
            print("Simbolo incorrecto")

    #funcion calcarea
    def siguiente_calc(self):
        archivo = 'Conteo_calcareas'
        mineral= [(self.input_cal_mineral.text())]
        size= [(self.input_cal_size.value())]
        redondez= [(self.input_cal_redond.currentText())]
        esfericidad= [(self.input_cal_esfer.currentText())]
        t_contacto= [(self.input_cal_contacto.currentText())]
        observaciones= [(self.input_cal_observa.toPlainText())]
        parametros = [mineral, size, redondez, esfericidad, t_contacto, observaciones]
        if agregar_puntos(archivo, parametros):
            self.input_cal_mineral.clear()
            self.input_cal_size.setValue(0)
            self.input_cal_redond.setCurrentText("Angular")
            self.input_cal_esfer.setCurrentText("Elongado")
            self.input_cal_contacto.setCurrentText("Tangencial")
            self.input_cal_observa.clear()
        else:
            print("Simbolo incorrecto")

    #funcion siliciclastica
    def siguiente_silici(self):
        archivo = 'Conteo_siliciclasticas'
        mineral = [(self.input_sil_mineral.text())]
        size = [(self.input_sil_size.value())]
        redondez =[(self.input_sil_redond.currentText())]
        esfericidad = [(self.input_sil_esfer.currentText())]
        t_contacto = [(self.input_sil_contacto.currentText())]
        observaciones = [(self.input_sil_observa.toPlainText())]
        parametros = [mineral, size, redondez, esfericidad, t_contacto, observaciones]
        if agregar_puntos(archivo, parametros):
            self.input_sil_mineral.clear()
            self.input_sil_size.setValue(0)
            self.input_sil_redond.setCurrentText("Angular")
            self.input_sil_esfer.setCurrentText("Elongado")
            self.input_sil_contacto.setCurrentText("Tangencial")
            self.input_sil_observa.clear()
        else:
            print("simbolo incorrecto")

    #funcion observaciones sedimentarias y metamorficas
    def observaciones(self):
        print(self.input_observaciones_gen.toPlainText())
        self.input_observaciones_gen.clear()

    #funcion observaciones igneas
    def observaciones_ig(self):
        print(self.input_size_relat_ig.currentText())
        print(self.input_size_absol_ig.currentText())
        print(self.input_textura_ig.currentText())
        print(self.input_indice_c.value())
        print(self.input_observaciones_gen_ig.toPlainText())
        self.input_observaciones_gen_ig.clear()
        self.input_indice_c.clear()
        self.input_size_relat_ig.setCurrentText("Equigranular")
        self.input_size_absol_ig.setCurrentText("Ultra fino")
        self.input_textura_ig.setCurrentText("Holocristalina")

    # funciones cargar fotos micro
    def cargar_ppl(self):
        ruta_ppl, foto_ppl = agregar_imagen()
        self.label_micro_ppl.setPixmap(foto_ppl)
        data = {"url_ppl" : [ruta_ppl]}
        llenado_csv('auxiliar_micro',data)

    def cargar_xpl(self):
        ruta_xpl, foto_xpl = agregar_imagen()
        self.label_micro_xpl.setPixmap(foto_xpl)
        data = {"url_xpl" : [ruta_xpl]}
        llenado_csv('auxiliar_micro',data)

    def guardar_descripcion_micro(self):
        descripcion  = self.input_descripcion_fotos_micro.toPlainText()
        data = {"descrpcion_micro": [descripcion]}
        llenado_csv('auxiliar_micro',data)
        self.input_descripcion_fotos_micro.clear()
        self.label_micro_xpl.clear()
        self.label_micro_ppl.clear()
        stack_micro_data()

    # exportaciones
    def export_csv(self):
        guardar_csv()
    
    def export_triangulo(self):
        print("los super triangulos")
    
    def export_histograma(self):
        print("|iL|")

    def export_formato(self):
        nombre_a = llenar_info_general()
        general = pd.read_csv("./archivos/current_general.csv", sep = ";", encoding= "latin")
        llenar_macro(nombre_a)

        if general["Subt_r"][0] == "Siliciclástica": llenar_inter_silici(nombre_a)
        elif general["Subt_r"][0] == "Calcárea": llenar_inter_silici(nombre_a)
        elif general["Subt_r"][0] == "Regional o de Contacto": llenar_inter_regional(nombre_a)
        elif general["Subt_r"][0] == "Dinámico": llenar_inter_dinamico(nombre_a)
        elif general["Subt_r"][0] == "Plutónica": llenar_inter_plut(nombre_a)
        elif general["Subt_r"][0] == "Volcánica": llenar_inter_plut(nombre_a)
        elif general["Subt_r"][0] == "Volcanoclástica": llenar_inter_plut(nombre_a)

        llenar_fotos_micro(nombre_a)
        


    # def read_parametros_conteo(self):
    #     mineral = self.input_mineral.text()
    #     redondez = self.input_redon.value()
    #     esfericidad = self.input_esfer.value()
    #     coor_x = self.input_coor_x.value()
    #     coor_y = self.input_coor_y.value()
    #     tamaño = self.input_size.value()
    #     escribir_archivo("./archivos/muestra.csv", [mineral, tamaño, 
    #                                     redondez, esfericidad, 
    #                                     coor_x, coor_y])
    #     self.actuarlizar_interfaz()
def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = interfaz()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # app.exec_()
    sys.exit(app.exec_())

main()

