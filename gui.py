import sys
import api_request as mtg
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication, QMainWindow, QApplication, QAction, qApp, QTextEdit, QLabel, QFileDialog, QGridLayout, QLineEdit)
from PyQt5.QtGui import QFont, QIcon

class App(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.lbl_deck = QLabel(u'''
        Carga un decklist\nen formato .txt
        ''')
        self.lbl_sim = QLabel(u'''
        Simulación no iniciada
        ''')
        self.lbl_carta = QLabel("Carta elegida:")
        
        self.btn_cargar = QPushButton("Cargar deklist", self)
        self.btn_cargar.clicked.connect(self.showDialog)
        
        self.btn_simular = QPushButton(u"Iniciar simulación")
        self.btn_simular.clicked.connect(self.iniciarSim)

        self.btn_cerrar = QPushButton("&Salir")
        self.btn_cerrar.setShortcut('Ctrl+Q')
        self.btn_cerrar.setStatusTip('Salir de la App')
        self.btn_cerrar.clicked.connect(qApp.quit)

        self.inp_cartas = QLineEdit()

        self.var_deck = False

        self.initUI()

    def initUI(self):
        newAct = QAction(QIcon("icons/file-plus.svg"), "Nuevo", self)
        newAct.setShortcut("Ctrl+N")
        newAct.setStatusTip("Nueva decklist")
        newAct.triggered.connect(self.showDialog)
        
        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.btn_cargar, 1, 0)
        grid.addWidget(self.btn_simular, 1, 1)
        grid.addWidget(self.lbl_carta, 2, 0)
        grid.addWidget(self.inp_cartas, 2, 1)
        grid.addWidget(self.lbl_deck, 3, 0)
        grid.addWidget(self.lbl_sim, 3, 1)
        grid.addWidget(self.btn_cerrar, 4, 0, 1, 2)

        self.setLayout(grid)
        
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('MTG App')
        self.setWindowIcon(QIcon('mtg_icon.png'))

        self.show()
    
    def showDialog(self):
        archivo = QFileDialog.getOpenFileName(self, "Nuevo decklist", "/home")
        if archivo[0]:
            deck_plain = mtg.leer_plain_deck(archivo[0])
            deck_text = mtg.get_decklist_text(deck_plain)
            deck_text = "".join(deck_text)

            self.lbl_deck.setText(deck_text)
            self.var_deck = mtg.generar_mazo(archivo[0])
    
    def iniciarSim(self):
        if isinstance(self.var_deck, dict):
            carta_buscada = "Light Up the Stage"
            sim_resultado = mtg.generar_simulacion(self.var_deck, carta_buscada)
            sim_texto = mtg.print_sim(sim_resultado)
            sim_texto = "Carta buscada: " + carta_buscada + "\n" + sim_texto
            self.lbl_sim.setText(sim_texto)
        else:
            self.lbl_sim.setText("Carga un deck")


class AppMenu(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
     
    def initMenu(self):
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

        toolbar = self.addToolBar("Archivo")
        toolbar.addAction(newAct)
        toolbar.addAction(guardarAct)
        toolbar.addAction(exitAct)
        toolbar = self.addToolBar("Simulacion")
        toolbar.addAction(simAct)

        self.setGeometry(10, 50, 200, 100)
        self.setLayout(toolbar)

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
