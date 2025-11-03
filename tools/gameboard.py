import sys
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QPushButton, QLabel, 
                             QFrame, QMessageBox)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QFont, QPalette, QColor
from .hall_of_fame import HallOfFameDialog
from .player_name_dialog import PlayerNameDialog

# Constantes del juego
ROWS = 5
COLS = 9
CELL_SIZE = 80

# Tipos de torres (Rooks)
ROOK_TYPES = {
    'BASIC': {'name': 'Básica', 'cost': 50, 'damage': 10, 'range': 1, 'color': '#3b82f6', 'icon': '🏰'},
    'ADVANCED': {'name': 'Avanzada', 'cost': 100, 'damage': 25, 'range': 2, 'color': '#8b5cf6', 'icon': '🗼'},
    'ELITE': {'name': 'Elite', 'cost': 200, 'damage': 50, 'range': 3, 'color': '#ec4899', 'icon': '👑'}
}

# Tipos de avatares (enemigos)
AVATAR_TYPES = {
    'BASIC': {'hp': 50, 'speed': 1000, 'reward': 25, 'color': '#ef4444', 'icon': '👾'},
    'TANK': {'hp': 100, 'speed': 2000, 'reward': 50, 'color': '#f59e0b', 'icon': '🛡️'},
    'FAST': {'hp': 30, 'speed': 500, 'reward': 30, 'color': '#10b981', 'icon': '⚡'}
}


class Cell(QFrame):
    """Representa una celda del tablero"""
    def __init__(self, row, col, parent=None):
        super().__init__(parent)
        self.row = row
        self.col = col
        self.content = None
        self.setFixedSize(CELL_SIZE, CELL_SIZE)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.setLineWidth(2)
        
        # Layout para el contenido
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.setLayout(self.layout)
        
        # Label para mostrar íconos
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont('Arial', 24))
        self.layout.addWidget(self.label)
        
        self.update_style()
    
    def update_style(self):
        """Actualiza el estilo de la celda"""
        if self.row == 0:
            # Zona crítica (fila superior)
            self.setStyleSheet("background-color: #fee2e2; border: 2px solid #ef4444;")
        elif self.content:
            if self.content['type'] == 'rook':
                color = self.content['data']['color']
                self.setStyleSheet(f"background-color: {color}40; border: 2px solid {color};")
            elif self.content['type'] == 'avatar':
                color = self.content['data']['color']
                self.setStyleSheet(f"background-color: {color}40; border: 2px solid {color};")
        else:
            self.setStyleSheet("background-color: #f0f9ff; border: 2px solid #bae6fd;")
    
    def set_content(self, content_type, data):
        """Establece el contenido de la celda"""
        self.content = {'type': content_type, 'data': data}
        if content_type == 'rook':
            self.label.setText(data['icon'])
        elif content_type == 'avatar':
            self.label.setText(data['icon'])
        self.update_style()
    
    def clear_content(self):
        """Limpia el contenido de la celda"""
        self.content = None
        self.label.setText('')
        self.update_style()


class Avatar:
    """Representa un enemigo (Avatar)"""
    def __init__(self, avatar_type, col, avatar_id):
        self.id = avatar_id
        self.type = avatar_type
        self.data = AVATAR_TYPES[avatar_type].copy()
        self.col = col
        self.row = ROWS - 1  # Comienza en la fila inferior
        self.hp = self.data['hp']
        self.max_hp = self.data['hp']
    
    def move_up(self):
        """Mueve el avatar una fila hacia arriba"""
        if self.row > 0:
            self.row -= 1
            return True
        return False
    
    def take_damage(self, damage):
        """El avatar recibe daño"""
        self.hp -= damage
        return self.hp <= 0  # Retorna True si fue eliminado


class Rook:
    """Representa una torre defensiva (Rook)"""
    def __init__(self, rook_type, row, col, rook_id):
        self.id = rook_id
        self.type = rook_type
        self.data = ROOK_TYPES[rook_type].copy()
        self.row = row
        self.col = col
        self.last_attack = 0
    
    def can_attack(self, avatar):
        """Verifica si la torre puede atacar al avatar"""
        distance = abs(self.row - avatar.row) + abs(self.col - avatar.col)
        return distance <= self.data['range']


class GameBoard(QMainWindow):
    """Ventana principal del juego"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Avatars VS Rooks - Nivel 1")
        self.setFixedSize(1200, 700)
        
        # Estado del juego
        self.coins = 200
        self.score = 0
        self.lives = 10
        self.wave = 1
        self.selected_rook = 'BASIC'
        self.game_running = False
        self.rooks = []
        self.avatars = []
        self.next_rook_id = 0
        self.next_avatar_id = 0
        
        # Timers
        self.game_timer = QTimer()
        self.game_timer.timeout.connect(self.game_loop)
        
        self.spawn_timer = QTimer()
        self.spawn_timer.timeout.connect(self.spawn_avatar)
        
        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.move_avatars)
        
        # Contador para controlar velocidad de movimiento
        self.move_counter = 0
        
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Panel izquierdo - Tablero
        board_layout = QVBoxLayout()
        
        # Crear el tablero (matriz 9x5)
        self.cells = []
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(2)
        
        for row in range(ROWS):
            row_cells = []
            for col in range(COLS):
                cell = Cell(row, col)
                cell.mousePressEvent = lambda event, r=row, c=col: self.cell_clicked(r, c)
                self.grid_layout.addWidget(cell, row, col)
                row_cells.append(cell)
            self.cells.append(row_cells)
        
        board_layout.addLayout(self.grid_layout)
        main_layout.addLayout(board_layout)
        
        # Panel derecho - Controles
        control_panel = QVBoxLayout()
        control_panel.setSpacing(15)
        
        # Información del juego
        title = QLabel("AVATARS VS ROOKS")
        title.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        control_panel.addWidget(title)
        
        # Stats
        self.coins_label = QLabel(f"💰 Monedas: {self.coins}")
        self.coins_label.setFont(QFont('Arial', 14))
        control_panel.addWidget(self.coins_label)
        
        self.score_label = QLabel(f"⭐ Puntos: {self.score}")
        self.score_label.setFont(QFont('Arial', 14))
        control_panel.addWidget(self.score_label)
        
        self.lives_label = QLabel(f"❤️ Vidas: {self.lives}")
        self.lives_label.setFont(QFont('Arial', 14))
        control_panel.addWidget(self.lives_label)
        
        self.wave_label = QLabel(f"🌊 Oleada: {self.wave}")
        self.wave_label.setFont(QFont('Arial', 14))
        control_panel.addWidget(self.wave_label)
        
        control_panel.addWidget(QLabel("─" * 30))
        
        # Selección de torres
        towers_label = QLabel("Selecciona Torre:")
        towers_label.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        control_panel.addWidget(towers_label)
        
        for rook_key, rook_data in ROOK_TYPES.items():
            btn = QPushButton(f"{rook_data['icon']} {rook_data['name']}\n💰 {rook_data['cost']} | ⚔️ {rook_data['damage']} | 📏 {rook_data['range']}")
            btn.setFixedHeight(60)
            btn.clicked.connect(lambda checked, key=rook_key: self.select_rook(key))
            control_panel.addWidget(btn)
        
        control_panel.addWidget(QLabel("─" * 30))
        
        # Botones de control
        self.start_btn = QPushButton("▶️ Iniciar Juego")
        self.start_btn.setFixedHeight(50)
        self.start_btn.setStyleSheet("background-color: #10b981; color: white; font-size: 14px; font-weight: bold;")
        self.start_btn.clicked.connect(self.start_game)
        control_panel.addWidget(self.start_btn)
        
        self.pause_btn = QPushButton("⏸️ Pausar")
        self.pause_btn.setFixedHeight(50)
        self.pause_btn.setEnabled(False)
        self.pause_btn.clicked.connect(self.pause_game)
        control_panel.addWidget(self.pause_btn)
        
        reset_btn = QPushButton("🔄 Reiniciar")
        reset_btn.setFixedHeight(50)
        reset_btn.clicked.connect(self.reset_game)
        control_panel.addWidget(reset_btn)
        
        control_panel.addStretch()
        
        # Info
        info_label = QLabel("Haz clic en una celda\npara colocar una torre")
        info_label.setFont(QFont('Arial', 10))
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("color: #6b7280; padding: 10px;")
        control_panel.addWidget(info_label)
        
        main_layout.addLayout(control_panel)
        main_layout.setStretch(0, 3)
        main_layout.setStretch(1, 1)
    
    def select_rook(self, rook_key):
        """Selecciona el tipo de torre a colocar"""
        self.selected_rook = rook_key
        QMessageBox.information(self, "Torre Seleccionada", 
                                f"Has seleccionado: {ROOK_TYPES[rook_key]['name']}")
    
    def cell_clicked(self, row, col):
        """Maneja el clic en una celda del tablero"""
        if not self.game_running:
            QMessageBox.warning(self, "Juego no iniciado", "Debes iniciar el juego primero")
            return
        
        cell = self.cells[row][col]
        
        # No se puede colocar en la fila superior (zona crítica)
        if row == 0:
            QMessageBox.warning(self, "Posición inválida", "No puedes colocar torres en la zona crítica")
            return
        
        # Verificar si la celda está vacía
        if cell.content is not None:
            QMessageBox.warning(self, "Posición ocupada", "Esta celda ya está ocupada")
            return
        
        # Verificar monedas
        rook_data = ROOK_TYPES[self.selected_rook]
        if self.coins < rook_data['cost']:
            QMessageBox.warning(self, "Monedas insuficientes", 
                                f"Necesitas {rook_data['cost']} monedas. Tienes: {self.coins}")
            return
        
        # Colocar la torre
        self.place_rook(row, col)
    
    def place_rook(self, row, col):
        """Coloca una torre en el tablero"""
        rook_data = ROOK_TYPES[self.selected_rook].copy()
        rook = Rook(self.selected_rook, row, col, self.next_rook_id)
        self.next_rook_id += 1
        
        self.rooks.append(rook)
        self.coins -= rook_data['cost']
        
        self.cells[row][col].set_content('rook', rook_data)
        self.update_ui()
    
    def start_game(self):
        """Inicia el juego"""
        self.game_running = True
        self.start_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        
        # Iniciar timers
        self.game_timer.start(100)  # Loop principal cada 100ms
        self.spawn_timer.start(3000)  # Generar avatar cada 3 segundos
        self.move_timer.start(1500)  # Mover avatares cada 1.5 segundos
    
    def pause_game(self):
        """Pausa el juego"""
        self.game_running = False
        self.game_timer.stop()
        self.spawn_timer.stop()
        self.move_timer.stop()
        self.start_btn.setEnabled(True)
        self.start_btn.setText("▶️ Continuar")
        self.pause_btn.setEnabled(False)
    
    def reset_game(self):
        """Reinicia el juego"""
        self.game_running = False
        self.game_timer.stop()
        self.spawn_timer.stop()
        self.move_timer.stop()
        
        # Limpiar tablero
        for row in self.cells:
            for cell in row:
                cell.clear_content()
        
        # Resetear estado
        self.coins = 200
        self.score = 0
        self.lives = 10
        self.wave = 1
        self.rooks = []
        self.avatars = []
        self.next_rook_id = 0
        self.next_avatar_id = 0
        self.move_counter = 0
        
        self.start_btn.setText("▶️ Iniciar Juego")
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        
        self.update_ui()
    
    def spawn_avatar(self):
        """Genera un avatar aleatorio"""
        if not self.game_running:
            return
        
        # Elegir tipo aleatorio
        avatar_type = random.choice(list(AVATAR_TYPES.keys()))
        col = random.randint(0, COLS - 1)
        
        # Verificar si la celda inferior está libre
        if self.cells[ROWS - 1][col].content is None:
            avatar = Avatar(avatar_type, col, self.next_avatar_id)
            self.next_avatar_id += 1
            self.avatars.append(avatar)
            
            avatar_data = AVATAR_TYPES[avatar_type]
            self.cells[ROWS - 1][col].set_content('avatar', avatar_data)
    
    def game_loop(self):
        """Loop principal del juego"""
        if not self.game_running:
            return
        
        # Torres atacan
        self.rooks_attack()
        
        # Actualizar UI
        self.update_ui()
        
        # Verificar fin del juego
        if self.lives <= 0:
            self.game_over()
    
    def move_avatars(self):
        """Mueve todos los avatares hacia arriba"""
        avatars_to_remove = []
        
        for avatar in self.avatars:
            old_row = avatar.row
            old_col = avatar.col
            
            # Limpiar posición anterior
            self.cells[old_row][old_col].clear_content()
            
            # Mover
            if not avatar.move_up():
                # Llegó a la zona crítica
                avatars_to_remove.append(avatar)
                self.lives -= 1
            else:
                # Actualizar nueva posición
                avatar_data = AVATAR_TYPES[avatar.type]
                self.cells[avatar.row][avatar.col].set_content('avatar', avatar_data)
        
        # Eliminar avatares que llegaron arriba
        for avatar in avatars_to_remove:
            self.avatars.remove(avatar)
    
    def rooks_attack(self):
        """Las torres atacan a los avatares en rango"""
        avatars_to_remove = []
        
        for rook in self.rooks:
            for avatar in self.avatars:
                if rook.can_attack(avatar):
                    if avatar.take_damage(rook.data['damage']):
                        # Avatar eliminado
                        avatars_to_remove.append(avatar)
                        self.coins += avatar.data['reward']
                        self.score += avatar.data['reward']
                        
                        # Limpiar celda
                        self.cells[avatar.row][avatar.col].clear_content()
                    break  # Una torre ataca a un avatar por turno
        
        # Eliminar avatares muertos
        for avatar in avatars_to_remove:
            if avatar in self.avatars:
                self.avatars.remove(avatar)
    
    def update_ui(self):
        """Actualiza los labels de la interfaz"""
        self.coins_label.setText(f"💰 Monedas: {self.coins}")
        self.score_label.setText(f"⭐ Puntos: {self.score}")
        self.lives_label.setText(f"❤️ Vidas: {self.lives}")
        self.wave_label.setText(f"🌊 Oleada: {self.wave}")
    
    def game_over(self):
        """Termina el juego"""
        self.pause_game()
        QMessageBox.information(self, "Game Over", 
                                f"¡Juego terminado!\n\nPuntuación final: {self.score}")


def main():
    app = QApplication(sys.argv)
    game = GameBoard()
    game.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()