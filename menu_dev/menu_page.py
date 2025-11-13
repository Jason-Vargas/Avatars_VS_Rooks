from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout

class MenuPage(QWidget):
    def __init__(self):
        super().__init__()
        self.btn_play = QPushButton("🎮  Jugar")
        self.btn_options = QPushButton("⚙️  Opciones")
        self.btn_info = QPushButton("ℹ️  Información")
        self.btn_wiki = QPushButton("📖  Wiki")
        self.btn_halloffame = QPushButton("🏆  Hall Of Fame")
        self.btn_exit = QPushButton("🚪  Salir")

        for b in (self.btn_play, self.btn_options, self.btn_info, 
                    self.btn_wiki, self.btn_halloffame, self.btn_exit):
            b.setMinimumHeight(44)
            b.setStyleSheet("border-radius:12px; font-size:16px;")

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.addStretch(1)
        layout.addWidget(self.btn_play)
        layout.addWidget(self.btn_options)
        layout.addWidget(self.btn_info)
        layout.addWidget(self.btn_wiki)
        layout.addWidget(self.btn_halloffame)
        layout.addWidget(self.btn_exit)
        layout.addStretch(1)

