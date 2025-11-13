from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class Tablero(QWidget):
    def __init__(self):
        super().__init__()
        self.filas = 9
        self.columnas = 5
        self.celdas = []
        self.init_ui()
    
    def init_ui(self):
        # Configurar ventana principal
        self.setWindowTitle("Matriz Postapocalíptica")
        self.setStyleSheet("background-color: #1a1a1a;")
        
        # Layout principal
        layout_principal = QVBoxLayout()
        
        # Título apocalíptico
        titulo = QLabel("◢ SISTEMA DE VIGILANCIA SECTOR 7 ◣")
        titulo.setFont(QFont("Courier", 12, QFont.Weight.Bold))
        titulo.setStyleSheet("color: #8b0000; padding: 10px;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(titulo)
        
        # Widget contenedor para la matriz
        contenedor_matriz = QWidget()
        contenedor_matriz.setStyleSheet("""
            background-color: #2d2d2d;
            border: 3px solid #4a3520;
            border-radius: 5px;
        """)
        
        # Grid layout para la matriz
        grid_layout = QGridLayout()
        grid_layout.setSpacing(3)
        grid_layout.setContentsMargins(10, 10, 10, 10)
        
        # Crear matriz 9x5
        for fila in range(self.filas):
            fila_celdas = []
            for col in range(self.columnas):
                celda = QLabel(f"[{fila},{col}]")
                celda.setFont(QFont("Courier", 11, QFont.Weight.Bold))
                celda.setAlignment(Qt.AlignmentFlag.AlignCenter)
                celda.setMinimumSize(100, 60)
                celda.setStyleSheet("""
                    QLabel {
                        background-color: #1c1c1c;
                        color: #6b8e23;
                        border: 2px inset #3d3d3d;
                        border-radius: 3px;
                        padding: 5px;
                    }
                    QLabel:hover {
                        background-color: #2a3a2a;
                        color: #9acd32;
                        border: 2px solid #4a5a2a;
                    }
                """)
                
                grid_layout.addWidget(celda, fila, col)
                fila_celdas.append(celda)
            
            self.celdas.append(fila_celdas)
        
        contenedor_matriz.setLayout(grid_layout)
        layout_principal.addWidget(contenedor_matriz)
        
        self.setLayout(layout_principal)
    
    def actualizar_celda(self, fila, col, texto):
        """Actualizar el contenido de una celda específica"""
        if 0 <= fila < self.filas and 0 <= col < self.columnas:
            self.celdas[fila][col].setText(texto)
    
    def obtener_celda(self, fila, col):
        """Obtener el widget de una celda específica"""
        if 0 <= fila < self.filas and 0 <= col < self.columnas:
            return self.celdas[fila][col]
        return None