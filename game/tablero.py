from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class Tablero(QWidget):
    def __init__(self):
        super().__init__()
        self.filas = 9
        self.columnas = 5
        self.sel_fila = 0
        self.sel_columna = 0
        self.celdas = []
        self.init_ui()
        self.celdas_rojas = []
        self.fila_roja(0)
        self.resaltar_celda(0, 0)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.colocar_rook_callback = None
        self.rook_seleccionada = 1  # valor por defecto


    
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
                """)
                
                grid_layout.addWidget(celda, fila, col)
                fila_celdas.append(celda)
            
            self.celdas.append(fila_celdas)
        
        contenedor_matriz.setLayout(grid_layout)
        layout_principal.addWidget(contenedor_matriz)
        
        self.setLayout(layout_principal)
    
    def resaltar_celda(self, fila, col):
        for f in range(self.filas):
            for c in range(self.columnas):
                if (f, c) in self.celdas_rojas:
                    self.celdas[f][c].setStyleSheet("""
                        background-color: #940901;
                        color: #630601;
                        border: 2px inset #630601;
                        border-radius: 3px;
                        padding: 5px;
                    """)
                    continue
                self.celdas[f][c].setStyleSheet("""
                    background-color: #1c1c1c;
                    color: #6b8e23;
                    border: 2px inset #3d3d3d;
                    border-radius: 3px;
                    padding: 5px;
                """)
        # Celda selecionada
        self.celdas[fila][col].setStyleSheet("""
            background-color: #3a2a2a;
            color: #ffcc00;
            border: 3px solid #ffcc00;
            border-radius: 3px;
            padding: 5px;
        """)
    def fila_roja(self, col):
        self.celdas_rojas = [(0, c) for c in range(self.columnas)]
        for c in range(self.columnas):
            self.celdas[0][c].setStyleSheet("""
                background-color: #940901;
                color: #630601;
                border: 2px inset #630601;
                border-radius: 3px;
                padding: 5px;
            """)
        
    def keyPressEvent(self, event):
        tecla = event.key()

        if tecla == Qt.Key.Key_Up:
            self.sel_fila = max(0, self.sel_fila - 1)
        elif tecla == Qt.Key.Key_Down:
            self.sel_fila = min(self.filas - 1, self.sel_fila + 1)
        elif tecla == Qt.Key.Key_Left:
            self.sel_columna = max(0, self.sel_columna - 1)
        elif tecla == Qt.Key.Key_Right:
            self.sel_columna = min(self.columnas - 1, self.sel_columna + 1)
        elif tecla == Qt.Key.Key_1:
            self.rook_seleccionada = 1
            print("Seleccionado: SandRook")
            return
        elif tecla == Qt.Key.Key_2:
            self.rook_seleccionada = 2
            print("Seleccionado: RockRook")
            return
        elif tecla == Qt.Key.Key_3:
            self.rook_seleccionada = 3
            print("Seleccionado: FireRook")
            return
        elif tecla == Qt.Key.Key_4:
            self.rook_seleccionada = 4
            print("Seleccionado: WaterRook")
            return
        elif tecla == Qt.Key.Key_X:  # ← NUEVO
            self.colocar_rook_en_seleccion()
            return
        elif event.key() == Qt.Key.Key_Z:
            print(f"Celda seleccionada: ({self.sel_fila}, {self.sel_columna})")
            return
        elif tecla == Qt.Key.Key_Escape:
            # Guardar la partida y salir
            if hasattr(self, "game_controller") and self.game_controller is not None:
                print("Guardar y salir (tecla ESC)...")
                # Llamamos al método del controlador
                self.game_controller.guardar_partida()
            else:
                print("No hay game_controller vinculado; no se puede guardar.")
            return
        elif event.key() == Qt.Key.Key_Z:
            print(f"Celda seleccionada: ({self.sel_fila}, {self.sel_columna})")
            return
        else:
            return

        self.resaltar_celda(self.sel_fila, self.sel_columna)

        

    def actualizar_celda(self, fila, col, texto):
        """Actualizar el contenido de una celda específica"""
        if 0 <= fila < self.filas and 0 <= col < self.columnas:
            self.celdas[fila][col].setText(texto)
    
    def obtener_celda(self, fila, col):
        """Obtener el widget de una celda específica"""
        if 0 <= fila < self.filas and 0 <= col < self.columnas:
            return self.celdas[fila][col]
        return None
    def colocar_rook_en_seleccion(self):
        if self.colocar_rook_callback:
            self.colocar_rook_callback(self.sel_fila, self.sel_columna, self.rook_seleccionada)

    def limpiar_tablero(self):
        for f in range(self.filas):
            for c in range(self.columnas):
                self.actualizar_celda(f, c, f"[{f},{c}]")

