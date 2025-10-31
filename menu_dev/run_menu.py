from PyQt6.QtWidgets import QApplication
from .menu_window import MenuWindow
import sys

print("[menu] starting")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MenuWindow()
    w.show()
    print("[menu] shown")
    sys.exit(app.exec())
