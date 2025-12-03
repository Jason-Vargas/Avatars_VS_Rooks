from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QPushButton, QLabel, QTableWidget, QTableWidgetItem,
                              QHeaderView, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
from app.database.mongo_connection import db
from datetime import datetime


class HallOfFameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏆 SALÓN DE LA FAMA")
        self.setMinimumSize(600, 500)
        self.collection = db["hall_of_fame"]
        
        # Widget central y layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Título
        title = QLabel("🏆 SALÓN DE LA FAMA 🏆")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #d4af37; margin-bottom: 10px;")
        main_layout.addWidget(title)
        
        # Subtítulo
        subtitle = QLabel("Jugadores que completaron el juego")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px; color: #666; margin-bottom: 10px;")
        main_layout.addWidget(subtitle)
        
        # Tabla
        self.setup_table()
        main_layout.addWidget(self.table)
        
        # Botones
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        self.btn_refresh = self.create_button("🔄 Actualizar", "#5b9bd5", "#4a7db0", self.refresh_data)
        self.btn_clear = self.create_button("🗑️ Limpiar Historial", "#e67e22", "#d35400", self.clear_history)
        self.btn_close = self.create_button("❌ Cerrar", "#95a5a6", "#7f8c8d", self.close)
        
        buttons_layout.addWidget(self.btn_refresh)
        buttons_layout.addWidget(self.btn_clear)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.btn_close)
        
        main_layout.addLayout(buttons_layout)
        
        # Cargar datos
        self.load_winners()
    
    def setup_table(self):
        """Configura la tabla de ganadores"""
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Posición", "Jugador", "Fecha"])
        
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #ddd;
                border-radius: 8px;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item { padding: 12px; }
            QHeaderView::section {
                background-color: #5b9bd5;
                color: white;
                padding: 12px;
                border: none;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    
    def create_button(self, text, bg_color, hover_color, callback):
        """Crea un botón estilizado"""
        btn = QPushButton(text)
        btn.setMinimumHeight(40)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {hover_color}; }}
        """)
        btn.clicked.connect(callback)
        return btn
    
    def load_winners(self):
        """Carga los ganadores desde MongoDB"""
        try:
            # Obtener ganadores ordenados por fecha (más reciente primero)
            winners = list(self.collection.find().sort("completed_at", -1))
            
            if not winners:
                self.show_empty_table()
                return
            
            self.table.setRowCount(len(winners))
            
            for row, winner in enumerate(winners):
                # Posición con medallas
                position_item = self.create_position_item(row)
                
                # Nombre del jugador
                name_item = QTableWidgetItem(winner.get("username", "Desconocido"))
                name_item.setFont(QFont("Arial", 12, QFont.Weight.Bold if row < 3 else QFont.Weight.Normal))
                
                # Fecha de completado
                completed_at = winner.get("completed_at")
                date_str = completed_at.strftime("%d/%m/%Y %H:%M") if completed_at else "N/A"
                date_item = QTableWidgetItem(date_str)
                date_item.setFont(QFont("Arial", 10))
                date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Aplicar color de podio
                if row < 3:
                    bg_color = self.get_podium_color(row)
                    name_item.setBackground(bg_color)
                    date_item.setBackground(bg_color)
                
                self.table.setItem(row, 0, position_item)
                self.table.setItem(row, 1, name_item)
                self.table.setItem(row, 2, date_item)
                self.table.setRowHeight(row, 50)
                
            print(f"✅ Cargados {len(winners)} ganadores")
            
        except Exception as e:
            print(f"❌ Error cargando ganadores: {e}")
            self.show_empty_table()
    
    def create_position_item(self, row):
        """Crea el item de posición con medallas"""
        position_item = QTableWidgetItem()
        
        if row == 0:
            position_item.setText(f"🥇 1º")
        elif row == 1:
            position_item.setText(f"🥈 2º")
        elif row == 2:
            position_item.setText(f"🥉 3º")
        else:
            position_item.setText(f"   {row + 1}º")
        
        position_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        position_item.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        
        if row < 3:
            position_item.setBackground(self.get_podium_color(row))
        
        return position_item
    
    def get_podium_color(self, position):
        """Retorna el color según la posición del podio"""
        colors = {
            0: QColor(255, 215, 0, 80),    # Oro
            1: QColor(192, 192, 192, 80),  # Plata
            2: QColor(205, 127, 50, 80)    # Bronce
        }
        return colors.get(position, QColor(255, 255, 255))
    
    def show_empty_table(self):
        """Muestra mensaje cuando no hay ganadores"""
        self.table.setRowCount(1)
        empty_item = QTableWidgetItem("No hay ganadores aún")
        empty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_item.setFont(QFont("Arial", 12))
        empty_item.setForeground(QColor(150, 150, 150))
        self.table.setSpan(0, 0, 1, 3)
        self.table.setItem(0, 0, empty_item)
        self.table.setRowHeight(0, 60)
    
    def refresh_data(self):
        """Actualiza los datos de la tabla"""
        print("🔄 Actualizando Hall of Fame...")
        self.load_winners()
    
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
            try:
                result = self.collection.delete_many({})
                print(f"🗑️ Eliminados {result.deleted_count} ganadores")
                self.load_winners()
                QMessageBox.information(
                    self,
                    "Historial Limpiado",
                    "El Salón de la Fama ha sido limpiado exitosamente."
                )
            except Exception as e:
                print(f"❌ Error limpiando historial: {e}")
                QMessageBox.critical(self, "Error", f"No se pudo limpiar el historial: {str(e)}")
    
    @staticmethod
    def add_winner(username):
        """Agrega un ganador al salón de la fama (método estático para usar desde cualquier parte)"""
        try:
            collection = db["hall_of_fame"]
            
            # Verificar si ya completó el juego
            if collection.find_one({"username": username}):
                print(f"ℹ️ {username} ya está en el Salón de la Fama")
                return False
            
            # Agregar nuevo ganador
            winner = {
                "username": username,
                "completed_at": datetime.now()
            }
            
            result = collection.insert_one(winner)
            
            if result.inserted_id:
                print(f"🏆 {username} agregado al Salón de la Fama!")
                return True
            return False
            
        except Exception as e:
            print(f"❌ Error agregando ganador: {e}")
            return False