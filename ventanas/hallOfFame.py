from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QPushButton, QLabel, QTableWidget, QTableWidgetItem,
                              QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor


class HallOfFameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏆 Hall of Fame")
        self.setMinimumSize(700, 500)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Título
        title = QLabel("🏆 HALL OF FAME 🏆")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #d4af37; margin-bottom: 10px;")
        main_layout.addWidget(title)
        
        # Subtítulo
        subtitle = QLabel("Los mejores jugadores de todos los tiempos")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px; color: #666; margin-bottom: 10px;")
        main_layout.addWidget(subtitle)
        
        # Tabla de clasificación
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Ranking", "Nombre", "Puntaje", "Oleadas"])
        
        # Estilo de la tabla
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #ddd;
                border-radius: 8px;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #5b9bd5;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 13px;
            }
        """)
        
        # Configurar el header
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        
        # Deshabilitar edición
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        # Selección por fila completa
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        # Cargar datos de ejemplo
        self.load_sample_data()
        
        main_layout.addWidget(self.table)
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        self.btn_refresh = QPushButton("🔄 Actualizar")
        self.btn_refresh.setMinimumHeight(40)
        self.btn_refresh.setStyleSheet("""
            QPushButton {
                background-color: #5b9bd5;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4a7db0;
            }
        """)
        self.btn_refresh.clicked.connect(self.refresh_data)
        
        self.btn_clear = QPushButton("🗑️ Limpiar Historial")
        self.btn_clear.setMinimumHeight(40)
        self.btn_clear.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """)
        self.btn_clear.clicked.connect(self.clear_history)
        
        self.btn_close = QPushButton("❌ Cerrar")
        self.btn_close.setMinimumHeight(40)
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
        
        buttons_layout.addWidget(self.btn_refresh)
        buttons_layout.addWidget(self.btn_clear)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.btn_close)
        
        main_layout.addLayout(buttons_layout)
    
    def load_sample_data(self):
        """Carga datos de ejemplo en la tabla"""
        # Datos de ejemplo (más adelante puedes cargarlos desde un archivo o base de datos)
        sample_data = [
            ("Juan Pérez", 15000, 25),
            ("María García", 12500, 22),
            ("Carlos López", 11000, 20),
            ("Ana Martínez", 9800, 18),
            ("Luis Rodríguez", 8500, 16),
            ("Sofia Fernández", 7200, 14),
            ("Diego Sánchez", 6800, 13),
            ("Laura Torres", 5900, 11),
            ("Miguel Ramírez", 5200, 10),
            ("Elena Castro", 4500, 9),
        ]
        
        self.table.setRowCount(len(sample_data))
        
        for row, (name, score, waves) in enumerate(sample_data):
            # Ranking con emoji de medalla para los primeros 3
            ranking_item = QTableWidgetItem()
            if row == 0:
                ranking_item.setText(f"🥇 {row + 1}")
                ranking_item.setBackground(QColor(255, 215, 0, 50))  # Dorado
            elif row == 1:
                ranking_item.setText(f"🥈 {row + 1}")
                ranking_item.setBackground(QColor(192, 192, 192, 50))  # Plateado
            elif row == 2:
                ranking_item.setText(f"🥉 {row + 1}")
                ranking_item.setBackground(QColor(205, 127, 50, 50))  # Bronce
            else:
                ranking_item.setText(f"   {row + 1}")
            
            ranking_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            ranking_item.setFont(QFont("Arial", 11, QFont.Weight.Bold))
            
            # Nombre
            name_item = QTableWidgetItem(name)
            name_item.setFont(QFont("Arial", 10))
            
            # Puntaje
            score_item = QTableWidgetItem(f"{score:,}")
            score_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            score_item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            score_item.setForeground(QColor(46, 125, 50))  # Verde oscuro
            
            # Oleadas
            waves_item = QTableWidgetItem(str(waves))
            waves_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            waves_item.setFont(QFont("Arial", 10))
            
            # Agregar items a la tabla
            self.table.setItem(row, 0, ranking_item)
            self.table.setItem(row, 1, name_item)
            self.table.setItem(row, 2, score_item)
            self.table.setItem(row, 3, waves_item)
            
            # Altura de fila
            self.table.setRowHeight(row, 45)
    
    def refresh_data(self):
        """Actualiza los datos de la tabla"""
        print("🔄 Actualizando Hall of Fame...")
        # Aquí puedes implementar la lógica para recargar datos desde un archivo o base de datos
        self.load_sample_data()
        print("✅ Hall of Fame actualizado")
    
    def clear_history(self):
        """Limpia el historial de puntuaciones"""
        print("🗑️ Limpiando historial...")
        self.table.setRowCount(0)
        print("✅ Historial limpiado")