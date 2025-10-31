from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("menu_dev/menu.ui", self)
        self.setWindowTitle("Menú principal")

        self.btn_play.clicked.connect(lambda: print("🎯 Iniciar juego…"))
        self.btn_options.clicked.connect(lambda: print("⚙️ Abrir opciones…"))
        self.btn_exit.clicked.connect(self.close)