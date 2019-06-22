import sys
import api_request as mtg
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtWidgets import (QAction, QActionGroup, QApplication, QFrame,
        QLabel, QMainWindow, QMenu, QMessageBox, QSizePolicy, QVBoxLayout,
        QWidget, QPushButton, QLineEdit, QFileDialog, qApp)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        widget = QWidget()
        self.setCentralWidget(widget)

        topFiller = QWidget()
        topFiller.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        bottomFiller = QWidget()
        bottomFiller.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.lbl_deck = QLabel("Carga un decklist en formato .txt")
        self.lbl_sim = QLabel("Simulación no iniciada")
        self.lbl_carta = QLabel('''
Elige cartas a buscar. 
Introduce los nombres separados por punto y coma (;).
        ''')

        self.btn_abrir = QPushButton("Abrir &deklist", self)
        self.btn_abrir.setStatusTip("Abrir decklist")
        self.btn_abrir.clicked.connect(self.showDialog)

        self.inp_cartas = QLineEdit()

        self.btn_simular = QPushButton(u"&Iniciar simulación")
        self.btn_simular.setStatusTip("Iniciar simulación")
        self.btn_simular.clicked.connect(self.iniciarSim)

        self.btn_cerrar = QPushButton("&Salir")
        self.btn_cerrar.setStatusTip("Salir")
        self.btn_cerrar.clicked.connect(qApp.quit)

        self.inp_cartas = QLineEdit()

        self.var_deck = False
        
        vbox = QVBoxLayout()
        vbox.setContentsMargins(5, 5, 5, 5)
        vbox.addWidget(topFiller)
        vbox.addWidget(self.btn_abrir)
        vbox.addWidget(self.lbl_carta)
        vbox.addWidget(self.inp_cartas)
        vbox.addWidget(self.btn_simular)
        vbox.addWidget(self.lbl_deck)
        vbox.addWidget(bottomFiller)
        vbox.addWidget(self.lbl_sim)
        vbox.addWidget(self.btn_cerrar)

        self.setWindowTitle("MTG App")
        self.setWindowIcon(QIcon("mtg_icon.png"))
        self.crearAcciones()
        self.crearMenus()
        self.crearToolbar()
        self.statusBar().showMessage("")
        widget.setLayout(vbox)

    def crearAcciones(self):
        self.abrirAct = QAction(QIcon("icons/file-plus.svg"), 
            "Abrir un &decklist", self, shortcut="Ctrl+D", statusTip="Abrir decklist")
        self.abrirAct.triggered.connect(self.showDialog)
        
        self.simAct = QAction(QIcon("icons/shuffle.svg"),
            "&Iniciar simulación", self, shortcut="Ctrl+I",
            statusTip="Iniciar simulación")
        self.simAct.triggered.connect(self.iniciarSim)

        self.salirAct = QAction(QIcon("icons/x-square.svg"),
            "Salir", self, shortcut="Ctrl+Q", 
            statusTip="Salir")
        self.salirAct.triggered.connect(qApp.quit)

    def crearMenus(self):
        self.fileMenu = self.menuBar().addMenu("&Archivo")
        self.fileMenu.addAction(self.abrirAct)
        self.fileMenu.addAction(self.simAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.salirAct)
    
    def crearToolbar(self):
        self.toolbar = self.addToolBar("Archivo")
        self.toolbar.addAction(self.abrirAct)
        self.toolbar.addAction(self.simAct)
        self.toolbar.addAction(self.salirAct)

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
            carta_input = self.inp_cartas.text()
            if ";" in carta_input:
                carta_iterable = carta_input.split(";")
                carta_buscada = []
                for elemento in carta_iterable:
                    carta_buscada.append(elemento.strip())
            else:
                carta_buscada = carta_input
            sim_resultado = mtg.generar_simulacion(self.var_deck, carta_buscada)
            sim_texto = mtg.print_sim(sim_resultado)
            sim_texto = "Carta buscada: " + carta_input + "\n" + sim_texto
            self.lbl_sim.setText(sim_texto)
        else:
            self.lbl_sim.setText("Carga un deck")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
