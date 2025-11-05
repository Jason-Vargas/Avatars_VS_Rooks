from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QPushButton, QLabel, QScrollArea, QDialog, QGridLayout,
                              QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap


class WikiWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📖 Wiki del Juego")
        self.setMinimumSize(900, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        title = QLabel("📖 WIKI DEL JUEGO")
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
                background-color: #f5f5f5;
            }
        """)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(20)
        
        # Sección de Torres
        scroll_layout.addWidget(self.create_section_title("🗼 TORRES"))
        scroll_layout.addWidget(self.create_items_grid(self.get_towers_data(), "tower"))
        
        # Sección de Avatars
        scroll_layout.addWidget(self.create_section_title("👤 AVATARS"))
        scroll_layout.addWidget(self.create_items_grid(self.get_avatars_data(), "avatar"))
        
        # Sección de Rooks
        scroll_layout.addWidget(self.create_section_title("♜ ROOKS"))
        scroll_layout.addWidget(self.create_items_grid(self.get_rooks_data(), "rook"))
        
        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)
        
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
        main_layout.addWidget(self.btn_close)
    
    def create_section_title(self, text):
        """Crea un título de sección"""
        label = QLabel(text)
        label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        label.setStyleSheet("""
            background-color: #34495e;
            color: white;
            padding: 10px;
            border-radius: 6px;
        """)
        return label
    
    def create_items_grid(self, items_data, item_type):
        """Crea una cuadrícula de items clickeables"""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        grid_layout = QGridLayout(container)
        grid_layout.setSpacing(15)
        
        row, col = 0, 0
        max_cols = 4
        
        for item in items_data:
            btn = QPushButton(f"{item['icon']} {item['name']}")
            btn.setMinimumHeight(60)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #ecf0f1;
                    border: 2px solid #bdc3c7;
                    border-radius: 8px;
                    font-size: 13px;
                    font-weight: bold;
                    text-align: left;
                    padding-left: 15px;
                }
                QPushButton:hover {
                    background-color: #3498db;
                    color: white;
                    border-color: #2980b9;
                }
            """)
            btn.clicked.connect(lambda checked, data=item, t=item_type: 
                               self.show_item_details(data, t))
            
            grid_layout.addWidget(btn, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        return container
    
    def get_towers_data(self):
        """Retorna los datos de las torres"""
        return [
            {
                "name": "Torre Arquera",
                "icon": "🏹",
                "damage": "15-25",
                "range": "Media",
                "speed": "Rápida",
                "cost": "100",
                "description": "Torre básica de ataque a distancia. Dispara flechas rápidas a enemigos individuales.",
                "special": "Crítico: 10% de probabilidad de hacer doble daño"
            },
            {
                "name": "Torre Mágica",
                "icon": "🔮",
                "damage": "30-40",
                "range": "Larga",
                "speed": "Lenta",
                "cost": "200",
                "description": "Torre de magia arcana. Lanza hechizos poderosos con área de efecto.",
                "special": "Daño de área: Afecta enemigos cercanos al objetivo"
            },
            {
                "name": "Torre de Fuego",
                "icon": "🔥",
                "damage": "20-30",
                "range": "Corta",
                "speed": "Media",
                "cost": "150",
                "description": "Torre que dispara bolas de fuego. Causa daño continuo por quemadura.",
                "special": "Quemadura: 5 daño por segundo durante 3 segundos"
            },
            {
                "name": "Torre de Hielo",
                "icon": "❄️",
                "damage": "10-15",
                "range": "Media",
                "speed": "Media",
                "cost": "175",
                "description": "Torre que congela a los enemigos, reduciendo su velocidad.",
                "special": "Congelamiento: Reduce velocidad enemiga en 50%"
            },
            {
                "name": "Torre Cañón",
                "icon": "💣",
                "damage": "50-70",
                "range": "Muy Larga",
                "speed": "Muy Lenta",
                "cost": "300",
                "description": "Torre de artillería pesada. Causa daño masivo pero con largo tiempo de recarga.",
                "special": "Explosión: Daño masivo en área grande"
            },
            {
                "name": "Torre Eléctrica",
                "icon": "⚡",
                "damage": "25-35",
                "range": "Media",
                "speed": "Rápida",
                "cost": "225",
                "description": "Torre que dispara rayos eléctricos que pueden saltar entre enemigos.",
                "special": "Cadena: El rayo salta hasta 3 enemigos adicionales"
            },
        ]
    
    def get_avatars_data(self):
        """Retorna los datos de los avatars"""
        return [
            {
                "name": "Guerrero",
                "icon": "⚔️",
                "hp": "200",
                "damage": "25-35",
                "speed": "Media",
                "ability": "Golpe Poderoso",
                "description": "Avatar equilibrado con buena defensa y ataque. Ideal para principiantes.",
                "special": "Golpe Poderoso: Causa 150% de daño cada 10 segundos"
            },
            {
                "name": "Mago",
                "icon": "🧙",
                "hp": "120",
                "damage": "40-50",
                "speed": "Lenta",
                "ability": "Teletransporte",
                "description": "Avatar de alto daño mágico pero frágil. Especialista en ataques a distancia.",
                "special": "Teletransporte: Puede moverse instantáneamente cada 15 segundos"
            },
            {
                "name": "Arquero",
                "icon": "🏹",
                "hp": "150",
                "damage": "20-30",
                "speed": "Rápida",
                "ability": "Lluvia de Flechas",
                "description": "Avatar rápido con ataques a distancia. Excelente movilidad.",
                "special": "Lluvia de Flechas: Dispara 10 flechas en área"
            },
            {
                "name": "Paladín",
                "icon": "🛡️",
                "hp": "300",
                "damage": "15-25",
                "speed": "Lenta",
                "ability": "Escudo Divino",
                "description": "Avatar tanque con alta resistencia. Perfecto para aguantar oleadas.",
                "special": "Escudo Divino: Inmune a daño durante 5 segundos"
            },
            {
                "name": "Asesino",
                "icon": "🗡️",
                "hp": "100",
                "damage": "50-70",
                "speed": "Muy Rápida",
                "ability": "Invisibilidad",
                "description": "Avatar de alto daño crítico y velocidad extrema. Alto riesgo, alta recompensa.",
                "special": "Invisibilidad: No recibe daño durante 3 segundos"
            },
            {
                "name": "Druida",
                "icon": "🌿",
                "hp": "180",
                "damage": "15-20",
                "speed": "Media",
                "ability": "Regeneración",
                "description": "Avatar de soporte con habilidades de curación y control de multitudes.",
                "special": "Regeneración: Recupera 10 HP por segundo durante 8 segundos"
            },
        ]
    
    def get_rooks_data(self):
        """Retorna los datos de los rooks (enemigos)"""
        return [
            {
                "name": "Rook Básico",
                "icon": "👾",
                "hp": "50",
                "damage": "5",
                "speed": "Media",
                "reward": "10 oro",
                "description": "Enemigo básico sin habilidades especiales. Aparece en oleadas tempranas.",
                "special": "Ninguna"
            },
            {
                "name": "Rook Rápido",
                "icon": "💨",
                "hp": "30",
                "damage": "3",
                "speed": "Muy Rápida",
                "reward": "15 oro",
                "description": "Enemigo veloz pero débil. Difícil de golpear pero fácil de eliminar.",
                "special": "Esquiva: 20% de probabilidad de evadir ataques"
            },
            {
                "name": "Rook Tanque",
                "icon": "🛡️",
                "hp": "200",
                "damage": "10",
                "speed": "Lenta",
                "reward": "30 oro",
                "description": "Enemigo resistente con mucha vida. Avanza lentamente pero aguanta mucho.",
                "special": "Armadura: Reduce el daño recibido en 30%"
            },
            {
                "name": "Rook Volador",
                "icon": "🦅",
                "hp": "40",
                "damage": "8",
                "speed": "Rápida",
                "reward": "20 oro",
                "description": "Enemigo aéreo que puede volar sobre obstáculos. Ignora el camino normal.",
                "special": "Vuelo: Puede atravesar torres y obstáculos"
            },
            {
                "name": "Rook Jefe",
                "icon": "👹",
                "hp": "500",
                "damage": "25",
                "speed": "Lenta",
                "reward": "100 oro",
                "description": "Jefe de oleada. Extremadamente resistente con habilidades especiales.",
                "special": "Regeneración: Recupera 5 HP por segundo"
            },
            {
                "name": "Rook Explosivo",
                "icon": "💥",
                "hp": "60",
                "damage": "15",
                "speed": "Media",
                "reward": "25 oro",
                "description": "Enemigo kamikaze que explota al morir, dañando torres cercanas.",
                "special": "Explosión: Causa 50 de daño al morir en área"
            },
            {
                "name": "Rook Mago",
                "icon": "🔮",
                "hp": "80",
                "damage": "20",
                "speed": "Lenta",
                "reward": "40 oro",
                "description": "Enemigo que lanza hechizos a distancia. Puede atacar torres desde lejos.",
                "special": "Hechizo: Ataca torres desde la distancia"
            },
            {
                "name": "Rook Sanador",
                "icon": "💚",
                "hp": "70",
                "damage": "5",
                "speed": "Media",
                "reward": "35 oro",
                "description": "Enemigo que cura a otros rooks cercanos. Prioridad alta de eliminación.",
                "special": "Curación: Restaura 10 HP a aliados cada 3 segundos"
            },
        ]
    
    def show_item_details(self, data, item_type):
        """Muestra una ventana con los detalles del item"""
        dialog = ItemDetailsDialog(data, item_type, self)
        dialog.exec()


class ItemDetailsDialog(QDialog):
    def __init__(self, data, item_type, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{data['icon']} {data['name']}")
        self.setMinimumSize(450, 400)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Título con icono
        title_layout = QHBoxLayout()
        icon_label = QLabel(data['icon'])
        icon_label.setFont(QFont("Arial", 48))
        title_label = QLabel(data['name'])
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title_layout.addWidget(icon_label)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        layout.addLayout(title_layout)
        
        # Línea separadora
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #bdc3c7;")
        layout.addWidget(line)
        
        # Estadísticas
        stats_widget = QFrame()
        stats_widget.setStyleSheet("""
            QFrame {
                background-color: #ecf0f1;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        stats_layout = QVBoxLayout(stats_widget)
        
        if item_type == "tower":
            stats_layout.addWidget(self.create_stat_label("💰 Costo:", data['cost']))
            stats_layout.addWidget(self.create_stat_label("⚔️ Daño:", data['damage']))
            stats_layout.addWidget(self.create_stat_label("📏 Alcance:", data['range']))
            stats_layout.addWidget(self.create_stat_label("⚡ Velocidad:", data['speed']))
        elif item_type == "avatar":
            stats_layout.addWidget(self.create_stat_label("❤️ Vida:", data['hp']))
            stats_layout.addWidget(self.create_stat_label("⚔️ Daño:", data['damage']))
            stats_layout.addWidget(self.create_stat_label("⚡ Velocidad:", data['speed']))
            stats_layout.addWidget(self.create_stat_label("✨ Habilidad:", data['ability']))
        elif item_type == "rook":
            stats_layout.addWidget(self.create_stat_label("❤️ Vida:", data['hp']))
            stats_layout.addWidget(self.create_stat_label("⚔️ Daño:", data['damage']))
            stats_layout.addWidget(self.create_stat_label("⚡ Velocidad:", data['speed']))
            stats_layout.addWidget(self.create_stat_label("💰 Recompensa:", data['reward']))
        
        layout.addWidget(stats_widget)
        
        # Descripción
        desc_label = QLabel("📝 Descripción:")
        desc_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        layout.addWidget(desc_label)
        
        desc_text = QLabel(data['description'])
        desc_text.setWordWrap(True)
        desc_text.setStyleSheet("""
            background-color: white;
            padding: 10px;
            border-radius: 6px;
            border: 1px solid #bdc3c7;
        """)
        layout.addWidget(desc_text)
        
        # Habilidad especial
        special_label = QLabel("⭐ Habilidad Especial:")
        special_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        layout.addWidget(special_label)
        
        special_text = QLabel(data['special'])
        special_text.setWordWrap(True)
        special_text.setStyleSheet("""
            background-color: #fff9e6;
            padding: 10px;
            border-radius: 6px;
            border: 2px solid #f39c12;
            color: #d68910;
            font-weight: bold;
        """)
        layout.addWidget(special_text)
        
        layout.addStretch()
        
        # Botón cerrar
        btn_close = QPushButton("✅ Entendido")
        btn_close.setMinimumHeight(40)
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)
    
    def create_stat_label(self, title, value):
        """Crea una etiqueta de estadística"""
        container = QHBoxLayout()
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        value_label = QLabel(str(value))
        value_label.setFont(QFont("Arial", 10))
        value_label.setStyleSheet("color: #2980b9;")
        
        container.addWidget(title_label)
        container.addWidget(value_label)
        container.addStretch()
        
        widget = QWidget()
        widget.setLayout(container)
        return widget