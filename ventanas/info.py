from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QPushButton, QLabel, QScrollArea, QFrame, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap


class InfoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ℹ️ Información del Juego")
        self.setMinimumSize(700, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Título principal
        title = QLabel("ℹ️ INFORMACIÓN DEL JUEGO")
        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        main_layout.addWidget(title)
        
        # Área de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #ecf0f1;
            }
        """)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(20)
        scroll_layout.setContentsMargins(15, 15, 15, 15)
        
        # Sección: Sobre el Juego
        scroll_layout.addWidget(self.create_info_section(
            "🎮 SOBRE EL JUEGO",
            """Este es un juego de defensa de torres (Tower Defense) donde debes proteger tu base 
de oleadas de enemigos cada vez más difíciles. Coloca estratégicamente tus torres, 
mejora tu avatar y sobrevive el mayor tiempo posible para alcanzar el Hall of Fame.

El objetivo es lograr la mayor puntuación posible sobreviviendo múltiples oleadas 
mientras administras tus recursos de manera inteligente."""
        ))
        
        # Sección: Equipo de Desarrollo
        creators_text = """
👨‍💻 Jason - Lead Developer & Game Design
👨‍💻 Ariel - Backend Developer & AI Logic
👨‍💻 Iván - Frontend Developer & UI/UX Design
👨‍💻 Alí - Graphics & Sound Designer
        """
        scroll_layout.addWidget(self.create_info_section(
            "👥 EQUIPO DE DESARROLLO",
            creators_text.strip()
        ))
        
        # Sección: Tecnologías Utilizadas
        scroll_layout.addWidget(self.create_tech_section())
        
        # Sección: Versión
        scroll_layout.addWidget(self.create_info_section(
            "📦 VERSIÓN DEL JUEGO",
            """Versión: 1.0.0 Beta
Fecha de Lanzamiento: Noviembre 2025
Estado: En desarrollo activo

Próximas actualizaciones:
- Nuevas torres y habilidades
- Modo multijugador
- Más tipos de enemigos
- Sistema de logros"""
        ))
        
        # Sección: Controles
        scroll_layout.addWidget(self.create_info_section(
            "🎮 CONTROLES",
            """🖱️ Click Izquierdo: Seleccionar y colocar torres
🖱️ Click Derecho: Cancelar selección
⌨️ Teclas 1-6: Selección rápida de torres
⌨️ ESC: Menú de pausa
⌨️ Espacio: Iniciar siguiente oleada
⌨️ WASD: Mover avatar (si está habilitado)"""
        ))
        
        # Sección: Cómo Jugar
        scroll_layout.addWidget(self.create_info_section(
            "📚 CÓMO JUGAR",
            """1️⃣ Coloca torres en el mapa para defender tu base
2️⃣ Cada torre tiene diferentes características (daño, alcance, velocidad)
3️⃣ Gana oro eliminando enemigos
4️⃣ Usa el oro para comprar y mejorar torres
5️⃣ Sobrevive oleadas progresivamente más difíciles
6️⃣ Mejora tu avatar para obtener habilidades especiales
7️⃣ Alcanza el puntaje más alto y entra al Hall of Fame"""
        ))
        
        # Sección: Créditos y Agradecimientos
        scroll_layout.addWidget(self.create_info_section(
            "🙏 CRÉDITOS Y AGRADECIMIENTOS",
            """Agradecimientos especiales a:
- PyQt6 Community por el framework GUI
- OpenGameArt por los recursos gráficos
- FreeSound por los efectos de sonido
- Todos los beta testers que nos ayudaron a mejorar

Música y Sonido:
- Biblioteca de sonidos: FreeSound.org
- Música de fondo: Compositor original

Assets Gráficos:
- Sprites personalizados creados por el equipo
- Iconos: Font Awesome & Custom Design"""
        ))
        
        # Sección: Contacto
        scroll_layout.addWidget(self.create_info_section(
            "📧 CONTACTO",
            """¿Encontraste un bug? ¿Tienes sugerencias?

📧 Email: support@towerdefense.com
🌐 Website: www.towerdefense.com
🐦 Twitter: @TowerDefenseGame
💬 Discord: discord.gg/towerdefense

¡Nos encantaría saber tu opinión!"""
        ))
        
        # Sección: Licencia
        scroll_layout.addWidget(self.create_info_section(
            "⚖️ LICENCIA",
            """© 2025 Tower Defense Game. Todos los derechos reservados.

Este juego es software propietario desarrollado por el equipo de Tower Defense.
No se permite la distribución, modificación o uso comercial sin autorización expresa.

Para consultas sobre licencias comerciales, contactar a: license@towerdefense.com"""
        ))
        
        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        # Botón de redes sociales (simulado)
        self.btn_social = QPushButton("🌐 Visitar Website")
        self.btn_social.setMinimumHeight(45)
        self.btn_social.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.btn_social.clicked.connect(self.open_website)
        
        # Botón de cerrar
        self.btn_close = QPushButton("❌ Cerrar")
        self.btn_close.setMinimumHeight(45)
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        self.btn_close.clicked.connect(self.close)
        
        buttons_layout.addWidget(self.btn_social)
        buttons_layout.addWidget(self.btn_close)
        main_layout.addLayout(buttons_layout)
    
    def create_info_section(self, title, content):
        """Crea una sección de información"""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 2px solid #bdc3c7;
            }
        """)
        
        layout = QVBoxLayout(container)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 15, 20, 15)
        
        # Título de la sección
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2c3e50; border: none;")
        layout.addWidget(title_label)
        
        # Línea separadora
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #bdc3c7; border: none;")
        layout.addWidget(line)
        
        # Contenido
        content_label = QLabel(content)
        content_label.setWordWrap(True)
        content_label.setFont(QFont("Arial", 10))
        content_label.setStyleSheet("color: #34495e; border: none; line-height: 1.6;")
        content_label.setTextFormat(Qt.TextFormat.PlainText)
        layout.addWidget(content_label)
        
        return container
    
    def create_tech_section(self):
        """Crea la sección de tecnologías con estilo especial"""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 2px solid #bdc3c7;
            }
        """)
        
        layout = QVBoxLayout(container)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 15, 20, 15)
        
        # Título
        title_label = QLabel("💻 TECNOLOGÍAS UTILIZADAS")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2c3e50; border: none;")
        layout.addWidget(title_label)
        
        # Línea separadora
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #bdc3c7; border: none;")
        layout.addWidget(line)
        
        # Tecnologías
        technologies = [
            ("🐍 Python 3.11", "Lenguaje de programación principal"),
            ("🖼️ PyQt6", "Framework para interfaz gráfica de usuario"),
            ("🎨 Qt Designer", "Diseño de interfaces visuales"),
            ("🎮 Pygame (Opcional)", "Motor de juego y gestión de sprites"),
            ("📊 NumPy", "Cálculos matemáticos y algoritmos"),
            ("🔊 PyAudio", "Gestión de audio y efectos de sonido"),
            ("💾 SQLite", "Base de datos para guardar puntuaciones"),
            ("📝 JSON", "Almacenamiento de configuración y datos"),
            ("🎯 Algoritmos A*", "Pathfinding para enemigos"),
            ("🏗️ Arquitectura MVC", "Patrón de diseño del código"),
        ]
        
        for tech, description in technologies:
            tech_widget = self.create_tech_item(tech, description)
            layout.addWidget(tech_widget)
        
        return container
    
    def create_tech_item(self, tech_name, description):
        """Crea un item de tecnología"""
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: #ecf0f1;
                border-radius: 6px;
                padding: 8px;
                border: none;
            }
        """)
        
        h_layout = QVBoxLayout(widget)
        h_layout.setSpacing(5)
        h_layout.setContentsMargins(10, 8, 10, 8)
        
        # Nombre de la tecnología
        name_label = QLabel(tech_name)
        name_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        name_label.setStyleSheet("color: #2980b9; border: none; background: transparent;")
        h_layout.addWidget(name_label)
        
        # Descripción
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Arial", 9))
        desc_label.setStyleSheet("color: #7f8c8d; border: none; background: transparent;")
        desc_label.setWordWrap(True)
        h_layout.addWidget(desc_label)
        
        return widget
    
    def open_website(self):
        """Simula abrir el website del juego"""
        print("🌐 Abriendo website del juego...")
        # Aquí podrías usar webbrowser.open() para abrir un URL real
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            "Website",
            "🌐 Website del juego:\nwww.towerdefense.com\n\n(Función simulada)"
        )