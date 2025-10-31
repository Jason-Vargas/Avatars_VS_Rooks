from PySide6.QtWidgets import QMainWindow, QMessageBox
from app.ui.ui_ventana_inicio import Ui_AvatarsVSRooks
from app.utils import auth

class VentanaInicio(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AvatarsVSRooks()
        self.ui.setupUi(self)
        self.setWindowTitle("Avatars VS Rooks - Login")

        # Widgets (usa los nombres reales del .ui)
        self.btn = getattr(self.ui, "btnEntrar", None) or getattr(self.ui, "Iniciar", None)
        self.txtUsuario = getattr(self.ui, "txtUsuario", None)
        self.txtPassword = getattr(self.ui, "txtPassword", None)

        if self.btn:
            self.btn.clicked.connect(self._on_login)
        if self.txtPassword and hasattr(self.txtPassword, "returnPressed"):
            self.txtPassword.returnPressed.connect(self._on_login)

    def _on_login(self):
        user = self.txtUsuario.text().strip() if self.txtUsuario else ""
        pwd  = self.txtPassword.text() if self.txtPassword else ""
        if not user or not pwd:
            self.statusBar().showMessage("Completa usuario y contraseña", 2000)
            QMessageBox.warning(self, "Login", "Completa usuario y contraseña.")
            return
        if auth.verify_user(user, pwd):
            self.statusBar().showMessage(f"Bienvenido, {user}", 2000)
            QMessageBox.information(self, "Login", "Acceso concedido.")
            # TODO: abrir menú principal aquí
        else:
            self.statusBar().showMessage("Credenciales inválidas", 2000)
            QMessageBox.critical(self, "Login", "Usuario o contraseña incorrectos.")
