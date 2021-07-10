from interfaz_grafica.interfaz_de_usuario import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
# from funciones.escritura_archivo import *
import sys
from funciones.archivo import *


class interfaz(Ui_MainWindow):
    def __init__( self ):
        super().__init__()

    
    def setupUi( self, MW ):
        super().setupUi( MW )

        self.hide_box()

        self.boton_guardar_tipo_roca.clicked.connect(self.guardar_tipo_roca)
        self.input_tipo_roca.currentTextChanged.connect(self.actualizar_despliegue)
        self.boton_agregar_mineral.clicked.connect(self.agregar_mineral)
        self.boton_ver_lista.clicked.connect(self.ver_lista)
        self.boton_guardar_calibracion.clicked.connect(self.calibracion)
        self.boton_guardar_interprete.clicked.connect(self.interprete)
        self.boton_guardar_info_muestra.clicked.connect(self.info_muetra)
        self.boton_cal_siguiente_p.clicked.connect(self.siguiente_calc)
        self.pushButton5.clicked.connect(self.visualizar_frame5)
        self.pushButton6.clicked.connect(self.visualizar_frame6)
        self.pushButton7.clicked.connect(self.visualizar_frame7)

    def hide_box(self):
        self.frame_calcarea.setVisible(False)
        self.frame_siliciclastica.setVisible(False)
        self.frame_pluton.setVisible(False)
        self.frame_5.setGeometry(QtCore.QRect(50,50,300,300))
        self.frame_6.setGeometry(QtCore.QRect(50,50,300,300))
        self.frame_7.setGeometry(QtCore.QRect(50,50,300,300))
    
    def visualizar_frame5(self):
        self.frame_5.setVisible(True)
        self.frame_6.setVisible(False)
        self.frame_7.setVisible(False)

    def visualizar_frame6(self):
        self.frame_5.setVisible(False)
        self.frame_6.setVisible(True)
        self.frame_7.setVisible(False)

    def visualizar_frame7(self):
        self.frame_5.setVisible(False)
        self.frame_6.setVisible(False)
        self.frame_7.setVisible(True)    

    def siguiente_calc(self):
        print(self.input_cal_mineral.text())
        self.input_cal_mineral.clear()
        print(self.input_cal_size.text())
        self.input_cal_size.clear()
        print(self.input_cal_redond.currentText())
        print(self.input_cal_esfer.currentText())
        print(self.input_cal_contacto.currentText())
        print(self.input_cal_observa.toPlainText())
        self.input_cal_observa.clear()

    def actualizar_despliegue(self):
        self.input_subtipo_roca.clear()
        if self.input_tipo_roca.currentText() == "Sedimentaria":
            list = ["Siliciclástica", "Calcarea"]
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

    def calibracion(self):
        print(self.input_objetivo.text())
        print(self.input_reticulas.text())
        self.input_reticulas.clear()
        self.input_objetivo.clear()

    def agregar_mineral(self):
        print(self.input_simbolo.text())
        print(self.input_mineral_config.text())
        self.input_mineral_config.clear()
        self.input_simbolo.clear()

    def ver_lista(self):
        print("aqui va una lista")

    def interprete(self):
        print(self.input_nombre_interprete.text())
        self.input_nombre_interprete.clear()
        print(self.input_fecha_analisis.text())

    def guardar_tipo_roca(self):

        print(self.input_tipo_roca.currentText())
        print(self.input_subtipo_roca.currentText())
        
    def info_muetra(self):
        print(self.input_igm.text())
        self.input_igm.clear()
        print(self.input_n_campo.text())
        self.input_n_campo.clear()
        print(self.input_unidad_lito.text())
        self.input_unidad_lito.clear()
        print(self.input_localidad.text())
        self.input_localidad.clear()
        print(self.input_departamento.text())
        self.input_departamento.clear()
        print(self.input_municipio.text())
        self.input_municipio.clear()
        print(self.input_plancha.text())
        self.input_plancha.clear()
        print(self.input_escala.text())
        self.input_escala.clear()
        print(self.input_origen.text())
        self.input_origen.clear()
        print(self.input_coor_x.text())
        self.input_coor_x.clear()
        print(self.input_coor_y.text())
        self.input_coor_y.clear()
        print(self.input_colector.text())
        self.input_colector.clear()
        print(self.input_fecha_recolec.text())
        #self.input_fecha_recolec.clear()
        print(self.input_cantidad_puntos.text())
        self.input_cantidad_puntos.clear()



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

    # def actuarlizar_interfaz(self):
    #     tabla_c = leer_archivo("./archivos/muestra.csv")
        
    #     self.input_size.clear()
    #     self.input_redon.clear()
    #     self.input_mineral.clear()
    #     self.input_esfer.clear()
    #     self.input_coor_x.clear()
    #     self.input_coor_y.clear()

    #     cantidad_puntos = tabla_c.shape[0]
    #     self.output_censo.display(cantidad_puntos)
        
    #     ultima_medicion = tabla_c.tail(1)

    #     for indice,variable in enumerate(ultima_medicion.columns) :
    #         celda = self.tabla_anterior.item(indice,1)
    #         celda.setText(str(ultima_medicion[variable].values[0]))
        
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = interfaz()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

main()

