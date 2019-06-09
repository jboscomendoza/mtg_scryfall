import sys
import api_request as mtg
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication, QMainWindow, QApplication, QAction, qApp, QTextEdit, QLabel, QFileDialog, QGridLayout, QLineEdit)
from PyQt5.QtGui import QFont, QIcon


class VentanaPrincipal(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("MTG App")
        self.setGeometry(300, 300, 300, 300)
        self.setWindowIcon(QIcon('mtg_icon.png'))

        self.initUI()
        
    def initUI(self):
        
        QToolTip.setFont(QFont('SansSerif', 10))
                
        newAct = QAction(QIcon("icons/file-plus.svg"), "Nuevo", self)
        newAct.setShortcut("Ctrl+N")
        newAct.setStatusTip("Nueva decklist")
        newAct.triggered.connect(self.showDialog)
        
        simAct = QAction(QIcon("icons/shuffle.svg"), "Simular", self)
        simAct.setShortcut("Ctrl+I")
        simAct.setStatusTip("Iniciar simulacion")
        
        guardarAct = QAction(QIcon("icons/save.svg"), "Guardar", self)
        guardarAct.setShortcut("Ctrl+G")
        guardarAct.setStatusTip("Guardar simulacion")

        exitAct = QAction(QIcon('icons/x-square.svg'), '&Salir', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Salir de la App')
        exitAct.triggered.connect(qApp.quit)

        self.statusBar().showMessage("Ok")
        
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

        self.red = RedLayout(self)
        self.setCentralWidget(self.red.initGrid())


        # boton = QPushButton('Boton para presionar', self)
        # boton.setToolTip('Este es un boton chido')
        # boton.resize(boton.sizeHint())
        # boton.move(50, 50)

        #boton_salida = QPushButton("Salir", self)
        #boton_salida.clicked.connect(QApplication.instance().quit)
        #boton_salida.setToolTip("Este boton cierra")
        #boton.resize(boton_salida.sizeHint())
        #boton.move(50, 50)
        
        self.show()
    
    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, "Nuevo decklist", "/home")
        if fname[0]:
            f = mtg.leer_decklist(fname[0])
            self.decklistEdit.setText(f[0][1])

class RedLayout(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
     
    def initGrid(self):
        
        lbl_decklist = QLabel('Decklist vacio', self)
        lbl_trials = QLabel("Numero de trials", self)
        edit_decklist = QLineEdit()
        edit_trials = QLineEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(lbl_decklist, 1, 0)
        grid.addWidget(edit_decklist, 1, 1)
        grid.addWidget(lbl_trials, 2, 0)
        grid.addWidget(edit_trials, 2, 1)

        self.setLayout(grid)

        self.setGeometry(10, 50, 200, 100)
        self.setLayout(grid)

        self.show()


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = VentanaPrincipal()
    sys.exit(app.exec_())