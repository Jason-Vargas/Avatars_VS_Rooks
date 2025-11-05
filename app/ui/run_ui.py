import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from ui_ventana_inicio import Ui_AvatarsVSRooks

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QMainWindow()
    ui = Ui_AvatarsVSRooks()
    ui.setupUi(win)
    win.show()
    sys.exit(app.exec())
