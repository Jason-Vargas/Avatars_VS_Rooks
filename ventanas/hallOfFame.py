from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QPushButton, QLabel, QTableWidget, QTableWidgetItem,
                              QHeaderView, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
from pathlib import Path
import json


class HallOfFameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏆 SALÓN DE LA FAMA")
        self.setMinimumSize(600, 500)
        
        # Ruta al archivo de ganadores
        self.winners_file = Path(__file__).parent.parent / "data" / "winners.json"
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Título
        title = QLabel("🏆 SALÓN DE LA FAMA 🏆")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #d4af37; margin-bottom: 10px;")
        main_layout.addWidget(title)
        
        # Subtítulo
        subtitle = QLabel("Jugadores que completaron el juego")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px; color: #666; margin-bottom: 10px;")
        main_layout.addWidget(subtitle)
        
        # Tabla de clasificación
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Posición", "Nombre del Jugador"])
        
        # Estilo de la tabla
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #ddd;
                border-radius: 8px;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 12px;
            }
            QHeaderView::section {
                background-color: #5b9bd5;
                color: white;
                padding: 12px;
                border: none;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        
        # Configurar el header
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        
        # Deshabilitar edición
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        # Selección por fila completa
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        # Cargar datos
        self.load_winners()
        
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
    
    def get_fake_winners(self):
        """Devuelve una lista de ganadores falsos para pruebas"""
        return [
            "DragonSlayer",
            "MasterChief",
            "ShadowNinja",
            "PhoenixRider",
            "IceQueen",
            "ThunderStrike",
            "CrimsonBlade",
            "SilverFox",
            "GoldenEagle",
            "DarkKnight",
            "StarGazer",
            "MoonWalker",
            "FireStorm",
            "OceanWave",
            "MountainKing"
        ]
    
    def load_winners_data(self):
        """Carga los ganadores desde el archivo JSON o devuelve datos falsos"""
        if self.winners_file.exists():
            try:
                with open(self.winners_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    winners = data.get('winners', [])
                    # Si está vacío, usar datos falsos
                    if not winners:
                        return self.get_fake_winners()
                    return winners
            except json.JSONDecodeError:
                print("⚠️ Error al leer archivo de ganadores, usando datos falsos")
                return self.get_fake_winners()
        else:
            # Si no existe el archivo, usar datos falsos
            print("ℹ️ Archivo no encontrado, usando datos de ejemplo")
            return self.get_fake_winners()
    
    def save_winners_data(self, winners):
        """Guarda los ganadores en el archivo JSON"""
        self.winners_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.winners_file, 'w', encoding='utf-8') as f:
            json.dump({"winners": winners}, f, indent=2, ensure_ascii=False)
    
    def load_winners(self):
        """Carga los ganadores en la tabla"""
        winners = self.load_winners_data()
        
        if not winners:
            self.table.setRowCount(1)
            empty_item = QTableWidgetItem("No hay ganadores aún")
            empty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_item.setFont(QFont("Arial", 12))
            empty_item.setForeground(QColor(150, 150, 150))
            self.table.setSpan(0, 0, 1, 2)
            self.table.setItem(0, 0, empty_item)
            self.table.setRowHeight(0, 60)
            return
        
        self.table.setRowCount(len(winners))
        
        for row, name in enumerate(winners):
            # Posición con emoji de medalla para los primeros 3
            position_item = QTableWidgetItem()
            if row == 0:
                position_item.setText(f"🥇 1º Lugar")
                position_item.setBackground(QColor(255, 215, 0, 80))  # Dorado
            elif row == 1:
                position_item.setText(f"🥈 2º Lugar")
                position_item.setBackground(QColor(192, 192, 192, 80))  # Plateado
            elif row == 2:
                position_item.setText(f"🥉 3º Lugar")
                position_item.setBackground(QColor(205, 127, 50, 80))  # Bronce
            else:
                position_item.setText(f"   {row + 1}º")
            
            position_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            position_item.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            
            # Nombre del jugador
            name_item = QTableWidgetItem(name)
            name_item.setFont(QFont("Arial", 12))
            
            # Resaltar el podio (primeros 3)
            if row < 3:
                name_item.setFont(QFont("Arial", 12, QFont.Weight.Bold))
                if row == 0:
                    name_item.setBackground(QColor(255, 215, 0, 80))
                elif row == 1:
                    name_item.setBackground(QColor(192, 192, 192, 80))
                elif row == 2:
                    name_item.setBackground(QColor(205, 127, 50, 80))
            
            # Agregar items a la tabla
            self.table.setItem(row, 0, position_item)
            self.table.setItem(row, 1, name_item)
            
            # Altura de fila
            self.table.setRowHeight(row, 50)
    
    def refresh_data(self):
        """Actualiza los datos de la tabla"""
        print("🔄 Actualizando Hall of Fame...")
        self.load_winners()
        print("✅ Hall of Fame actualizado")
    
    def clear_history(self):
        """Limpia el historial de ganadores"""
        reply = QMessageBox.question(
            self,
            "Confirmar",
            "¿Estás seguro de que quieres eliminar todos los ganadores del Salón de la Fama?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            print("🗑️ Limpiando historial...")
            self.save_winners_data([])
            self.load_winners()
            print("✅ Historial limpiado")
            QMessageBox.information(
                self,
                "Historial Limpiado",
                "El Salón de la Fama ha sido limpiado exitosamente."
            )
    
    def add_winner(self, username):
        """Agrega un ganador al salón de la fama"""
        winners = self.load_winners_data()
        
        # Si tenemos datos falsos, limpiar primero
        fake_winners = self.get_fake_winners()
        if winners == fake_winners:
            winners = []
        
        # Verificar si ya está en la lista
        if username not in winners:
            winners.append(username)
            self.save_winners_data(winners)
            print(f"🏆 {username} agregado al Salón de la Fama!")
            return True
        else:
            print(f"ℹ️ {username} ya está en el Salón de la Fama")
            return False