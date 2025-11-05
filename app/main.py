from PySide6.QtWidgets import QApplication
from app.ui.ventana_inicio import LoginWindow
import sys
from tools.music_manager import music



if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    music.play()
    sys.exit(app.exec())