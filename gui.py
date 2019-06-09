import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication, QMainWindow, QApplication, QAction, qApp)
from PyQt5.QtGui import QFont, QIcon


class Example(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        
        QToolTip.setFont(QFont('SansSerif', 10))
        
        exitAct = QAction('&Salir', self)        
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Salir de la App')
        exitAct.triggered.connect(qApp.quit)
        
        newAct = QAction("Nuevo", self)
        newAct.setShortcut("Ctrl+N")
        newAct.setStatusTip("Nueva decklist")
        
        simAct = QAction("Simular", self)
        simAct.setShortcut("Ctrl+I")
        simAct.setStatusTip("Iniciar simulacion")
        
        guardarAct = QAction("Guardar", self)
        guardarAct.setShortcut("Ctrl+G")
        guardarAct.setStatusTip("Guardar simulacion")

        self.statusBar().showMessage("Estado")
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&Archivo")
        fileMenu.addAction(newAct)
        fileMenu.addAction(guardarAct)
        fileMenu.addAction(exitAct)
        simMenu = menubar.addMenu("&Simulacion")
        simMenu.addAction(simAct)
        
        self.toolbar = self.addToolBar("Archivo")
        self.toolbar.addAction(newAct)
        self.toolbar.addAction(guardarAct)
        self.toolbar.addAction(exitAct)
        self.toolbar = self.addToolBar("Siimulacion")
        self.toolbar.addAction(simAct)

        # boton = QPushButton('Boton para presionar', self)
        # boton.setToolTip('Este es un boton chido')
        # boton.resize(boton.sizeHint())
        # boton.move(50, 50)

        #boton_salida = QPushButton("Salir", self)
        #boton_salida.clicked.connect(QApplication.instance().quit)
        #boton_salida.setToolTip("Este boton cierra")
        #boton.resize(boton_salida.sizeHint())
        #boton.move(50, 50)

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('MTG App')
        self.setWindowIcon(QIcon('mtg_icon.png'))
        
        self.show()
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())