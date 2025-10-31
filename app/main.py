import sys
from PySide6.QtWidgets import QApplication
from app.views.ventana_inicio import VentanaInicio

def main():
    app = QApplication(sys.argv)
    w = VentanaInicio()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
