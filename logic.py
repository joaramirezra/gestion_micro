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
        self.boton_siguiente.clicked.connect(self.read_parametros_conteo)
        
    def read_parametros_conteo(self):
        mineral = self.input_mineral.text()
        redondez = self.input_redon.value()
        esfericidad = self.input_esfer.value()
        coor_x = self.input_coor_x.value()
        coor_y = self.input_coor_y.value()
        tamaño = self.input_size.value()
        escribir_archivo("./archivos/muestra.csv", [mineral, tamaño, 
                                        redondez, esfericidad, 
                                        coor_x, coor_y])
        self.actuarlizar_interfaz()

    def actuarlizar_interfaz(self):
        tabla_c = leer_archivo("./archivos/muestra.csv")
        
        self.input_size.clear()
        self.input_redon.clear()
        self.input_mineral.clear()
        self.input_esfer.clear()
        self.input_coor_x.clear()
        self.input_coor_y.clear()

        cantidad_puntos = tabla_c.shape[0]
        self.output_censo.display(cantidad_puntos)
        
        ultima_medicion = tabla_c.tail(1)

        for indice,variable in enumerate(ultima_medicion.columns) :
            celda = self.tabla_anterior.item(indice,1)
            celda.setText(str(ultima_medicion[variable].values[0]))
        
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = interfaz()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

main()

