from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtGui import QPixmap
from pathlib import Path
from app.ui.ui_ventana_inicio import Ui_AvatarsVSRooks
from app.utils.auth import verify_user
from menu_dev.menu_window import MenuWindow

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AvatarsVSRooks()
        self.ui.setupUi(self)
        
        # Configurar imagen de fondo
        image_path = Path(__file__).parent.parent / "ui" / "images" / "fondo.jpg"
        
        print(f"🔍 Buscando imagen en: {image_path}")
        print(f"📁 ¿Existe? {image_path.exists()}")
        
        if image_path.exists():
            pixmap = QPixmap(str(image_path))
            self.ui.fondo.setPixmap(pixmap)
            self.ui.fondo.setScaledContents(True)
            print("✅ Imagen cargada correctamente")
        else:
            print(f"❌ Imagen no encontrada en: {image_path}")
        
        self.ui.btnEntrar.clicked.connect(self.handle_login)
        self.menu_window = None
    
    def handle_login(self):
        username = self.ui.txtUsuario.text()
        password = self.ui.txtPassword.text()
        
        if verify_user(username, password):
            print(f"✅ Login exitoso para: {username}")
            
            self.menu_window = MenuWindow()
            self.menu_window.show()
            self.close()
        else:
            QMessageBox.warning(
                self,
                "Error de autenticación",
                "Usuario o contraseña incorrectos"
            )
            self.ui.txtPassword.clear()
            self.ui.txtPassword.setFocus()