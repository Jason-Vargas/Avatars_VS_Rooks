from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtGui import QPixmap
from pathlib import Path
import json
import hashlib
import base64
import os
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
        self.ui.btn_registrarse.clicked.connect(self.handle_register)
        self.menu_window = None
        
        # Ruta al archivo JSON
        self.users_file = Path(__file__).parent.parent.parent / "data" / "users.json"
        
        # Configuración de hash
        self.iterations = 130000
    
    def load_users_data(self):
        """Carga los datos completos del archivo JSON"""
        if self.users_file.exists():
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"⚠️ Error al leer JSON, archivo corrupto")
                return {"users": []}
        return {"users": []}
    
    def save_users_data(self, data):
        """Guarda los datos en el archivo JSON"""
        # Crear directorio si no existe
        self.users_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def hash_password(self, password, salt=None):
        """Hashea la contraseña con PBKDF2"""
        if salt is None:
            salt = os.urandom(16)
        else:
            salt = base64.b64decode(salt)
        
        # Usar PBKDF2 con SHA256
        pwd_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            self.iterations
        )
        
        return {
            'salt': base64.b64encode(salt).decode('utf-8'),
            'hash': base64.b64encode(pwd_hash).decode('utf-8')
        }
    
    def user_exists(self, username):
        """Verifica si el usuario ya existe"""
        data = self.load_users_data()
        users = data.get('users', [])
        
        return any(user.get('username') == username for user in users)
    
    def handle_register(self):
        """Maneja el registro de nuevos usuarios"""
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
        
        # Verificar si el usuario ya existe
        if self.user_exists(username):
            QMessageBox.warning(
                self,
                "Usuario existente",
                f"El usuario '{username}' ya está registrado"
            )
            return
        
        # Hashear la contraseña
        hashed = self.hash_password(password)
        
        # Crear nuevo usuario
        data = self.load_users_data()
        new_user = {
            "username": username,
            "salt": hashed['salt'],
            "hash": hashed['hash'],
            "iterations": self.iterations,
            "role": "user",
            "active": True
        }
        
        data['users'].append(new_user)
        
        try:
            self.save_users_data(data)
            QMessageBox.information(
                self,
                "Registro exitoso",
                f"Usuario '{username}' registrado correctamente.\n¡Ahora puedes iniciar sesión!"
            )
            self.ui.txtPassword.clear()
            self.ui.txtUsuario.clear()
            self.ui.txtUsuario.setFocus()
            print(f"✅ Usuario registrado: {username}")
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo registrar el usuario: {str(e)}"
            )
            print(f"❌ Error al registrar: {e}")
    
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