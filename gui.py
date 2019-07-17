import sys
import mtg
import re
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QIcon, QPixmap
from PyQt5.QtWidgets import (QAction, QActionGroup, QApplication, QFrame,
        QLabel, QMainWindow, QMenu, QMessageBox, QSizePolicy, QVBoxLayout,
        QWidget, QPushButton, QLineEdit, QFileDialog, qApp, QGridLayout, QHBoxLayout,
        QComboBox, QTextEdit)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setStyleSheet(open("style.qss", "r").read())

        self.var_deck = False
        self.var_reps = 10

        ventanaApp = QWidget()
        self.setCentralWidget(ventanaApp)

        self.widget_abrir = self.crearWidgetAbrir()
        self.widget_rep = self.crearWidgetRep()
        self.widget_simular = self.crearWidgetSimular()
        self.widget_pic = self.crearWidgetPic()

        self.btn_cerrar = QPushButton("&Salir")
        self.btn_cerrar.setStatusTip("Salir")
        self.btn_cerrar.clicked.connect(qApp.quit)

        red_main = QGridLayout()
        red_main.setContentsMargins(5, 5, 5, 5)
        red_main.addWidget(self.widget_abrir,   0, 0)
        red_main.addWidget(self.widget_simular, 0, 1)
        red_main.addWidget(self.widget_pic,     0, 2)
        red_main.addWidget(self.btn_cerrar, 4, 0, 1, 3)

        self.setWindowTitle("MTG App")
        self.setWindowIcon(QIcon("mtg_icon.png"))
        self.crearAcciones()
        self.crearMenus()
        self.crearToolbar()
        self.statusBar().showMessage("")
        
        ventanaApp.setLayout(red_main)

    def crearRed(self, texto):
        self.mi_red = QGridLayout()
        # cant, nombre, costo, tipo, rareza, precio
        stats = 6
        n_cartas = int(len(texto) / stats)
        n_cartas = range(n_cartas)
        n_stats = range(stats)
        posiciones = [(renglon, columna) for renglon in n_cartas for columna in n_stats]
        for posicion, stat in zip(posiciones, texto):
            # Crea links
            if posicion[0] > 0 and posicion[1] == 1:
                stat = "<a href=none>" + stat + "</a>"
                label = QLabel(stat)
                label.linkActivated.connect(self.cambiar_pic)
            else:
                label = QLabel(str(stat))
            self.mi_red.addWidget(label, *posicion)

    def crearWidgetPic(self):
        widget_pic = QWidget()
        self.pic_carta = QLabel()
        self.pic_pixmap = QPixmap("carta_reverso.jpg")
        self.pic_pixmap = self.pic_pixmap.scaledToHeight(550)
        self.pic_carta.setPixmap(self.pic_pixmap)
        relleno = QWidget()
        relleno.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        box_pic = QVBoxLayout()
        box_pic.addWidget(self.pic_carta)
        box_pic.addWidget(relleno)
        widget_pic.setLayout(box_pic)
        return(widget_pic)

    def crearWidgetAbrir(self):
        widget_abrir = QWidget()
        relleno = QWidget()
        relleno.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn_abrir = QPushButton("Abrir &deklist", self)
        btn_abrir.setStatusTip("Abrir decklist en formato txt para MTGO")
        btn_abrir.clicked.connect(self.showDialog)
        self.lbl_deck = QLabel("Decklists en formato .txt para MTGO.")
        self.lbl_deck.setAlignment(Qt.AlignCenter)
        self.crearRed(texto="")
        self.widget_red = QWidget()
        box_abrir = QVBoxLayout()
        box_abrir.addWidget(btn_abrir)
        box_abrir.addWidget(self.lbl_deck)
        box_abrir.addWidget(self.widget_red)
        box_abrir.addWidget(relleno)
        widget_abrir.setLayout(box_abrir)
        return(widget_abrir)

    def crearWidgetRep(self):
        widget_rep = QWidget()
        lbl_rep_desc = QLabel(u"Número de iteraciones:")
        combo_rep = QComboBox()
        combo_rep.addItem("10")
        combo_rep.addItem("100")
        combo_rep.addItem("1000")
        combo_rep.addItem("10000")
        combo_rep.addItem("100000")
        combo_rep.activated[str].connect(self.eligeReps)
        hbox_conteo = QHBoxLayout()
        hbox_conteo.addWidget(lbl_rep_desc)
        hbox_conteo.addWidget(combo_rep)
        widget_rep.setLayout(hbox_conteo)
        return(widget_rep)
    
    def crearWidgetSimular(self):
        widget_simular = QWidget()
        btn_simular = QPushButton(u"&Iniciar simulación")
        btn_simular.setStatusTip(u"Iniciar simulación")
        btn_simular.clicked.connect(self.iniciarSim)
        lbl_carta = QLabel("Elige cartas a buscar, separadas por ;")
        self.inp_cartas = QLineEdit()
        self.lbl_sim = QLabel()
        relleno = QWidget()
        relleno.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        box_cartas = QVBoxLayout()
        box_cartas.addWidget(btn_simular)
        box_cartas.addWidget(lbl_carta)
        box_cartas.addWidget(self.inp_cartas)
        box_cartas.addWidget(self.widget_rep)
        box_cartas.addWidget(self.lbl_sim)
        box_cartas.addWidget(relleno)
        widget_simular.setLayout(box_cartas)
        return(widget_simular)

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
        self.toolbar.setMovable(False)
        self.toolbar.addAction(self.abrirAct)
        self.toolbar.addAction(self.simAct)
        self.toolbar.addAction(self.salirAct)

    def showDialog(self):
        mensaje_error = "<b>Decklist inválido. Verifica tu archivo.</b>"
        archivo = QFileDialog.getOpenFileName(self, "Abrir decklist", "/home", 
            "Archivos decklists (*.txt *.dec *.mwDeck)")
        if archivo[0]:
            self.var_deck = mtg.generar_mazo(archivo[0])
        if isinstance(self.var_deck, str):
            self.lbl_deck.setText(mensaje_error)
        else:
            decklist_text = self.var_deck["decklist_text"]
            self.lbl_deck.setText("Decklist abierto.")
            self.lbl_deck.clear()
            self.crearRed(texto=decklist_text)
            self.widget_red.setLayout(self.mi_red)

    def eligeReps(self, opcion):
        self.var_reps = int(opcion)

    def cambiar_pic(self):
        sender = self.sender()
        nombre_carta = sender.text()
        nombre_carta = re.sub("<.*?>", "", nombre_carta)
        carta_pic = mtg.get_carta_pic(nombre_carta)
        carta_pic = ImageQt(carta_pic)
        carta_pixmap = QPixmap.fromImage(carta_pic)
        carta_pixmap = carta_pixmap.scaledToHeight(550)
        self.pic_carta.setPixmap(carta_pixmap)
        return("ok")

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
            sim_resultado = mtg.generar_simulacion(self.var_deck, carta_buscada, 
                reps=self.var_reps)
            sim_texto = mtg.print_sim(sim_resultado)
            sim_texto = "Cartas buscadas: " + carta_input + "\n" + sim_texto
            self.lbl_sim.setText(sim_texto)
        else:
            self.lbl_sim.setText("Abre un decklist para iniciar simulación.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
