from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtGui import QPixmap
from pathlib import Path
from app.ui.ui_ventana_inicio import Ui_AvatarsVSRooks
from app.utils.auth import verify_user, register_user
from app.database.mongo_connection import test_connection
from menu_dev.menu_window import MenuWindow

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AvatarsVSRooks()
        self.ui.setupUi(self)
        
        # Verificar conexión a MongoDB al iniciar
        if not test_connection():
            QMessageBox.critical(
                self,
                "Error de conexión",
                "No se pudo conectar a la base de datos.\nVerifica tu conexión a internet."
            )
        
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
        
        # Conectar botones
        self.ui.btnEntrar.clicked.connect(self.handle_login)
        self.ui.btn_registrarse.clicked.connect(self.handle_register)
        self.menu_window = None
    
    def handle_register(self):
        """Maneja el registro de nuevos usuarios en MongoDB"""
        username = self.ui.txtUsuario.text().strip()
        password = self.ui.txtPassword.text().strip()
        
        # Validaciones
        if not username or not password:
            QMessageBox.warning(
                self,
                "Campos vacíos",
                "Por favor ingresa usuario y contraseña"
            )
            return
        
        if len(username) < 3:
            QMessageBox.warning(
                self,
                "Usuario inválido",
                "El usuario debe tener al menos 3 caracteres"
            )
            return
        
        if len(password) < 4:
            QMessageBox.warning(
                self,
                "Contraseña débil",
                "La contraseña debe tener al menos 4 caracteres"
            )
            return
        
        # Intentar registrar en MongoDB
        success, message = register_user(username, password)
        
        if success:
            QMessageBox.information(
                self,
                "Registro exitoso",
                f"Usuario '{username}' registrado correctamente.\n¡Ahora puedes iniciar sesión!"
            )
            self.ui.txtPassword.clear()
            self.ui.txtUsuario.clear()
            self.ui.txtUsuario.setFocus()
        else:
            QMessageBox.warning(
                self,
                "Error de registro",
                message
            )
    
    def handle_login(self):
        """Maneja el inicio de sesión con MongoDB"""
        username = self.ui.txtUsuario.text().strip()
        password = self.ui.txtPassword.text().strip()
        
        # Validaciones básicas
        if not username or not password:
            QMessageBox.warning(
                self,
                "Campos vacíos",
                "Por favor ingresa usuario y contraseña"
            )
            return
        
        # Verificar credenciales en MongoDB
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