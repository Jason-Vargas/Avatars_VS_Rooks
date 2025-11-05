import sys
import random
import os
import json
from pathlib import Path

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QPushButton, QLabel, 
                             QFrame, QMessageBox, QDialog, QLineEdit, 
                             QTableWidget, QTableWidgetItem, QFileDialog,
                             QSlider, QCheckBox, QComboBox)
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QFont, QAction
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

# Constantes del juego
ROWS = 5
COLS = 9
CELL_SIZE = 80
DATA_DIR = Path.home() / '.avatars_vs_rooks'
SCORES_FILE = DATA_DIR / 'scores.json'
SETTINGS_FILE = DATA_DIR / 'settings.json'

# Crear directorio de datos si no existe
DATA_DIR.mkdir(exist_ok=True)

# Configuración de niveles
LEVELS = {
    1: {
        'name': 'Principiante',
        'description': 'Nivel fácil para comenzar',
        'initial_coins': 250,
        'initial_lives': 15,
        'waves': 5,
        'spawn_interval': 3000,
        'move_interval': 1500,
        'avatars_per_wave_base': 8,
        'boss_wave': 5,
        'color': '#10b981'
    },
    2: {
        'name': 'Intermedio',
        'description': 'Mayor desafío y enemigos más fuertes',
        'initial_coins': 200,
        'initial_lives': 12,
        'waves': 8,
        'spawn_interval': 2500,
        'move_interval': 1200,
        'avatars_per_wave_base': 12,
        'boss_wave': 4,
        'color': '#f59e0b'
    },
    3: {
        'name': 'Experto',
        'description': 'Máxima dificultad - Solo para maestros',
        'initial_coins': 150,
        'initial_lives': 10,
        'waves': 12,
        'spawn_interval': 2000,
        'move_interval': 1000,
        'avatars_per_wave_base': 15,
        'boss_wave': 3,
        'color': '#ef4444'
    }
}

# Tipos de torres (Rooks)
ROOK_TYPES = {
    'BASIC': {'name': 'Básica', 'cost': 50, 'damage': 10, 'range': 1, 'color': '#3b82f6', 'icon': '🏰', 'attack_speed': 1.0},
    'ADVANCED': {'name': 'Avanzada', 'cost': 100, 'damage': 24, 'range': 2, 'color': '#8b5cf6', 'icon': '🗼', 'attack_speed': 1.2},
    'ELITE': {'name': 'Elite', 'cost': 200, 'damage': 50, 'range': 3, 'color': '#ec4899', 'icon': '👑', 'attack_speed': 1.5}
}

# Tipos de avatares (enemigos)
AVATAR_TYPES = {
    'BASIC': {'hp': 50, 'speed': 1000, 'reward': 25, 'color': '#ef4444', 'icon': '👾'},
    'TANK': {'hp': 120, 'speed': 2000, 'reward': 50, 'color': '#f59e0b', 'icon': '🛡️'},
    'FAST': {'hp': 30, 'speed': 500, 'reward': 35, 'color': '#10b981', 'icon': '⚡'},
    'BOSS': {'hp': 300, 'speed': 1500, 'reward': 150, 'color': '#dc2626', 'icon': '💀'}
}


class ScoreManager:
    """Gestiona el Hall of Fame"""
    
    @staticmethod
    def load_scores():
        """Carga las puntuaciones guardadas"""
        if SCORES_FILE.exists():
            try:
                with open(SCORES_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data
            except Exception as e:
                print(f"Error cargando puntuaciones: {e}")
                return []
        return []
    
    @staticmethod
    def save_score(name, score, wave, level):
        """Guarda una nueva puntuación"""
        try:
            DATA_DIR.mkdir(exist_ok=True)
            
            scores = ScoreManager.load_scores()
            
            import datetime
            scores.append({
                'name': name,
                'score': score,
                'wave': wave,
                'level': level,
                'level_name': LEVELS[level]['name'],
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            scores.sort(key=lambda x: x['score'], reverse=True)
            scores = scores[:20]  # Top 20 para tener más variedad
            
            with open(SCORES_FILE, 'w', encoding='utf-8') as f:
                json.dump(scores, f, indent=2, ensure_ascii=False)
            
            print(f"Puntuación guardada: {name} - {score} pts - Wave {wave} - Level {level}")
            
            return scores
        except Exception as e:
            print(f"Error guardando puntuación: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    @staticmethod
    def get_rank(score):
        """Obtiene el ranking de una puntuación"""
        scores = ScoreManager.load_scores()
        rank = 1
        for s in scores:
            if score > s['score']:
                return rank
            rank += 1
        return rank


class SettingsManager:
    """Gestiona las configuraciones del juego"""
    
    @staticmethod
    def load_settings():
        """Carga la configuración"""
        default_settings = {
            'music_enabled': True,
            'music_volume': 50,
            'music_file': None
        }
        
        if SETTINGS_FILE.exists():
            try:
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    default_settings.update(loaded)
            except:
                pass
        
        return default_settings
    
    @staticmethod
    def save_settings(settings):
        """Guarda la configuración"""
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2)


class HallOfFameDialog(QDialog):
    """Diálogo para mostrar el Hall of Fame"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🏆 Hall of Fame")
        self.setFixedSize(600, 450)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel("🏆 HALL OF FAME 🏆")
        title.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Tabla de puntuaciones
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['#', 'Jugador', 'Puntos', 'Oleada', 'Nivel'])
        self.table.horizontalHeader().setStretchLastSection(True)
        
        # Cargar puntuaciones
        scores = ScoreManager.load_scores()
        self.table.setRowCount(len(scores))
        
        for i, score in enumerate(scores):
            self.table.setItem(i, 0, QTableWidgetItem(f"#{i+1}"))
            self.table.setItem(i, 1, QTableWidgetItem(score['name']))
            self.table.setItem(i, 2, QTableWidgetItem(str(score['score'])))
            self.table.setItem(i, 3, QTableWidgetItem(str(score['wave'])))
            level_name = score.get('level_name', f"Nivel {score.get('level', 1)}")
            self.table.setItem(i, 4, QTableWidgetItem(level_name))
        
        layout.addWidget(self.table)
        
        # Botón cerrar
        close_btn = QPushButton("Cerrar")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)


class LevelSelectDialog(QDialog):
    """Diálogo para seleccionar el nivel"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar Nivel")
        self.setFixedSize(450, 400)
        self.selected_level = 1
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel("🎮 SELECCIONA EL NIVEL")
        title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Elige la dificultad del desafío")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #6b7280; margin-bottom: 10px;")
        layout.addWidget(subtitle)
        
        # Botones de nivel
        for level_num, level_data in LEVELS.items():
            btn_layout = QVBoxLayout()
            
            level_btn = QPushButton(f"NIVEL {level_num}: {level_data['name']}")
            level_btn.setFixedHeight(80)
            level_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {level_data['color']};
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 10px;
                }}
                QPushButton:hover {{
                    background-color: {level_data['color']}dd;
                }}
            """)
            level_btn.clicked.connect(lambda checked, l=level_num: self.select_level(l))
            
            # Info del nivel
            info_text = (
                f"💰 Monedas iniciales: {level_data['initial_coins']} | "
                f"❤️ Vidas: {level_data['initial_lives']} | "
                f"🌊 Oleadas: {level_data['waves']}\n"
                f"{level_data['description']}"
            )
            info_label = QLabel(info_text)
            info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            info_label.setStyleSheet("font-size: 11px; color: #4b5563; margin-bottom: 10px;")
            info_label.setWordWrap(True)
            
            layout.addWidget(level_btn)
            layout.addWidget(info_label)
        
        layout.addStretch()
        
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)
        
        self.setLayout(layout)
    
    def select_level(self, level):
        self.selected_level = level
        self.accept()
    
    def get_level(self):
        return self.selected_level


class PlayerNameDialog(QDialog):
    """Diálogo para ingresar el nombre del jugador"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nuevo Juego")
        self.setFixedSize(300, 150)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        label = QLabel("Ingresa tu nombre:")
        label.setFont(QFont('Arial', 12))
        layout.addWidget(label)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Tu nombre aquí...")
        self.name_input.setMaxLength(20)
        layout.addWidget(self.name_input)
        
        btn_layout = QHBoxLayout()
        
        ok_btn = QPushButton("Aceptar")
        ok_btn.clicked.connect(self.validate_and_accept)
        btn_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    def validate_and_accept(self):
        name = self.name_input.text().strip()
        if name:
            self.accept()
        else:
            QMessageBox.warning(self, "Nombre requerido", "Debes ingresar un nombre")
    
    def get_name(self):
        return self.name_input.text().strip()


class SettingsDialog(QDialog):
    """Diálogo de configuración"""
    
    def __init__(self, parent=None, current_settings=None):
        super().__init__(parent)
        self.setWindowTitle("⚙️ Configuración")
        self.setFixedSize(400, 250)
        self.settings = current_settings or SettingsManager.load_settings()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel("⚙️ CONFIGURACIÓN")
        title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        self.music_check = QCheckBox("Habilitar música")
        self.music_check.setChecked(self.settings['music_enabled'])
        self.music_check.stateChanged.connect(self.toggle_music_controls)
        layout.addWidget(self.music_check)
        
        vol_layout = QHBoxLayout()
        vol_label = QLabel("Volumen:")
        vol_layout.addWidget(vol_label)
        
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(self.settings['music_volume'])
        self.volume_slider.valueChanged.connect(self.update_volume_label)
        vol_layout.addWidget(self.volume_slider)
        
        self.volume_label = QLabel(f"{self.settings['music_volume']}%")
        vol_layout.addWidget(self.volume_label)
        
        layout.addLayout(vol_layout)
        
        music_btn = QPushButton("📁 Seleccionar archivo de música")
        music_btn.clicked.connect(self.select_music_file)
        layout.addWidget(music_btn)
        
        self.music_file_label = QLabel()
        if self.settings['music_file']:
            self.music_file_label.setText(f"Archivo: {Path(self.settings['music_file']).name}")
        else:
            self.music_file_label.setText("Sin archivo seleccionado")
        self.music_file_label.setStyleSheet("color: #6b7280; font-size: 10px;")
        layout.addWidget(self.music_file_label)
        
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton("Guardar")
        save_btn.clicked.connect(self.save_settings)
        btn_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        
        self.setLayout(layout)
        self.toggle_music_controls()
    
    def toggle_music_controls(self):
        enabled = self.music_check.isChecked()
        self.volume_slider.setEnabled(enabled)
    
    def update_volume_label(self, value):
        self.volume_label.setText(f"{value}%")
    
    def select_music_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo de música",
            "",
            "Audio Files (*.mp3 *.wav *.ogg);;All Files (*.*)"
        )
        
        if file_path:
            self.settings['music_file'] = file_path
            self.music_file_label.setText(f"Archivo: {Path(file_path).name}")
    
    def save_settings(self):
        self.settings['music_enabled'] = self.music_check.isChecked()
        self.settings['music_volume'] = self.volume_slider.value()
        SettingsManager.save_settings(self.settings)
        self.accept()
    
    def get_settings(self):
        return self.settings


class UpgradeDialog(QDialog):
    """Diálogo para mejorar torres"""
    
    def __init__(self, parent, rook, player_coins):
        super().__init__(parent)
        self.rook = rook
        self.player_coins = player_coins
        self.upgrade_choice = None
        self.setWindowTitle("🔧 Mejorar Torre")
        self.setFixedSize(350, 300)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel(f"🔧 Mejorar Torre {ROOK_TYPES[self.rook.type]['name']}")
        title.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        info = QLabel(
            f"Daño actual: {self.rook.data['damage']}\n"
            f"Rango actual: {self.rook.data['range']}\n"
            f"Nivel: {self.rook.upgrade_level}"
        )
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)
        
        coins_label = QLabel(f"💰 Monedas disponibles: {self.player_coins}")
        coins_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(coins_label)
        
        layout.addWidget(QLabel("─" * 40))
        
        upgrade_cost = 50 + (self.rook.upgrade_level * 25)
        
        damage_btn = QPushButton(f"⚔️ Mejorar Daño (+10)\n💰 Costo: {upgrade_cost}")
        damage_btn.clicked.connect(lambda: self.select_upgrade('damage', upgrade_cost))
        if self.player_coins < upgrade_cost:
            damage_btn.setEnabled(False)
        layout.addWidget(damage_btn)
        
        range_cost = upgrade_cost + 25
        range_btn = QPushButton(f"📏 Mejorar Rango (+1)\n💰 Costo: {range_cost}")
        range_btn.clicked.connect(lambda: self.select_upgrade('range', range_cost))
        if self.player_coins < range_cost or self.rook.data['range'] >= 5:
            range_btn.setEnabled(False)
        layout.addWidget(range_btn)
        
        speed_cost = upgrade_cost + 15
        speed_btn = QPushButton(f"⚡ Mejorar Velocidad (+20%)\n💰 Costo: {speed_cost}")
        speed_btn.clicked.connect(lambda: self.select_upgrade('speed', speed_cost))
        if self.player_coins < speed_cost:
            speed_btn.setEnabled(False)
        layout.addWidget(speed_btn)
        
        layout.addWidget(QLabel("─" * 40))
        
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)
        
        self.setLayout(layout)
    
    def select_upgrade(self, upgrade_type, cost):
        self.upgrade_choice = {'type': upgrade_type, 'cost': cost}
        self.accept()
    
    def get_upgrade(self):
        return self.upgrade_choice


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
        
        layout = QVBoxLayout()
        layout.setContentsMargins(2, 2, 2, 2)
        self.setLayout(layout)
        
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont('Arial', 24))
        layout.addWidget(self.label)
        
        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setFont(QFont('Arial', 8))
        self.info_label.setStyleSheet("color: white;")
        layout.addWidget(self.info_label)
        
        self.update_style()
    
    def update_style(self):
        if self.row == 0:
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
    
    def set_content(self, content_type, data, extra_info=""):
        self.content = {'type': content_type, 'data': data}
        if content_type == 'rook':
            self.label.setText(data['icon'])
            self.info_label.setText(extra_info)
        elif content_type == 'avatar':
            self.label.setText(data['icon'])
            self.info_label.setText(extra_info)
        self.update_style()
    
    def clear_content(self):
        self.content = None
        self.label.setText('')
        self.info_label.setText('')
        self.update_style()


class Avatar:
    """Representa un enemigo"""
    
    def __init__(self, avatar_type, col, avatar_id):
        self.id = avatar_id
        self.type = avatar_type
        self.data = AVATAR_TYPES[avatar_type].copy()
        self.col = col
        self.row = ROWS - 1
        self.hp = self.data['hp']
        self.max_hp = self.data['hp']
    
    def move_up(self):
        """Mueve el avatar una fila hacia arriba"""
        if self.row > 0:
            self.row -= 1
            return True
        return False
    
    def take_damage(self, damage):
        self.hp -= damage
        return self.hp <= 0

class Rook:
    """Representa una torre"""
    
    def __init__(self, rook_type, row, col, rook_id):
        self.id = rook_id
        self.type = rook_type
        self.data = ROOK_TYPES[rook_type].copy()
        self.row = row
        self.col = col
        self.last_attack = 0
        self.upgrade_level = 1
    
    def can_attack(self, avatar):
        distance = abs(self.row - avatar.row) + abs(self.col - avatar.col)
        return distance <= self.data['range']
    
    def upgrade(self, upgrade_type):
        """Mejora la torre"""
        if upgrade_type == 'damage':
            self.data['damage'] += 10
        elif upgrade_type == 'range':
            self.data['range'] += 1
        elif upgrade_type == 'speed':
            self.data['attack_speed'] *= 1.2
        
        self.upgrade_level += 1


class GameBoard(QMainWindow):
    """Ventana principal del juego"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Avatars VS Rooks - Tower Defense")
        self.setFixedSize(1200, 700)
        
        # Estado del juego
        self.current_level = 1
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
        self.player_name = None
        self.avatars_spawned = 0
        self.avatars_per_wave = 10
        self.max_waves = 5
        
        # Configuración
        self.settings = SettingsManager.load_settings()
        
        # Reproductor de música
        self.audio_output = QAudioOutput()
        self.music_player = QMediaPlayer()
        self.music_player.setAudioOutput(self.audio_output)
        self.music_player.setLoops(QMediaPlayer.Loops.Infinite)
        self.apply_audio_settings()
        
        # Timers
        self.game_timer = QTimer()
        self.game_timer.timeout.connect(self.game_loop)
        
        self.spawn_timer = QTimer()
        self.spawn_timer.timeout.connect(self.spawn_avatar)
        
        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.move_avatars)
        
        self.init_ui()
        self.create_menu_bar()
    
    def apply_audio_settings(self):
        """Aplica la configuración de audio"""
        volume = self.settings['music_volume'] / 100.0
        self.audio_output.setVolume(volume)
        
        if self.settings['music_enabled'] and self.settings['music_file']:
            if Path(self.settings['music_file']).exists():
                self.music_player.setSource(QUrl.fromLocalFile(self.settings['music_file']))
                self.music_player.play()
        else:
            self.music_player.stop()
    
    def apply_level_settings(self):
        """Aplica la configuración del nivel seleccionado"""
        level_config = LEVELS[self.current_level]
        self.coins = level_config['initial_coins']
        self.lives = level_config['initial_lives']
        self.max_waves = level_config['waves']
        
        # Actualizar timers según el nivel
        if hasattr(self, 'spawn_timer') and hasattr(self, 'move_timer'):
            self.spawn_timer.setInterval(level_config['spawn_interval'])
            self.move_timer.setInterval(level_config['move_interval'])
        
        self.avatars_per_wave = level_config['avatars_per_wave_base']
        
        # Actualizar título
        level_name = level_config['name']
        self.setWindowTitle(f"Avatars VS Rooks - Nivel {self.current_level}: {level_name}")
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        game_menu = menubar.addMenu('Juego')
        
        new_game_action = QAction('Nuevo Juego', self)
        new_game_action.triggered.connect(self.new_game)
        game_menu.addAction(new_game_action)
        
        game_menu.addSeparator()
        
        settings_action = QAction('⚙️ Configuración', self)
        settings_action.triggered.connect(self.show_settings)
        game_menu.addAction(settings_action)
        
        game_menu.addSeparator()
        
        exit_action = QAction('Salir', self)
        exit_action.triggered.connect(self.close)
        game_menu.addAction(exit_action)
        
        hof_menu = menubar.addMenu('Hall of Fame')
        
        view_hof_action = QAction('🏆 Ver Hall of Fame', self)
        view_hof_action.triggered.connect(self.show_hall_of_fame)
        hof_menu.addAction(view_hof_action)
    
    def show_settings(self):
        """Muestra el diálogo de configuración"""
        dialog = SettingsDialog(self, self.settings)
        if dialog.exec():
            self.settings = dialog.get_settings()
            self.apply_audio_settings()
    
    def new_game(self):
        if self.game_running or self.score > 0:
            reply = QMessageBox.question(self, 'Confirmar', 
                                        '¿Deseas iniciar un nuevo juego? Se perderá el progreso actual.',
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                return
        
        # Primero seleccionar nivel
        level_dialog = LevelSelectDialog(self)
        if not level_dialog.exec():
            return
        
        self.current_level = level_dialog.get_level()
        
        # Luego solicitar nombre
        dialog = PlayerNameDialog(self)
        if dialog.exec():
            self.player_name = dialog.get_name()
            self.reset_game()
            level_config = LEVELS[self.current_level]
            QMessageBox.information(self, "Nuevo Juego", 
                                   f"¡Buena suerte, {self.player_name}!\n\n"
                                   f"Nivel: {level_config['name']}\n"
                                   f"💰 Monedas: {level_config['initial_coins']}\n"
                                   f"❤️ Vidas: {level_config['initial_lives']}\n"
                                   f"🌊 Oleadas: {level_config['waves']}\n\n"
                                   "Haz clic en 'Iniciar Juego' cuando estés listo.\n"
                                   "Click derecho en torres para mejorarlas.")
    
    def show_hall_of_fame(self):
        dialog = HallOfFameDialog(self)
        dialog.exec()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Tablero
        board_layout = QVBoxLayout()
        
        self.cells = []
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(2)
        
        for row in range(ROWS):
            row_cells = []
            for col in range(COLS):
                cell = Cell(row, col)
                cell.mousePressEvent = lambda event, r=row, c=col: self.cell_clicked(event, r, c)
                self.grid_layout.addWidget(cell, row, col)
                row_cells.append(cell)
            self.cells.append(row_cells)
        
        board_layout.addLayout(self.grid_layout)
        main_layout.addLayout(board_layout)
        
        # Panel de control
        control_panel = QVBoxLayout()
        control_panel.setSpacing(15)
        
        title = QLabel("AVATARS VS ROOKS")
        title.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        control_panel.addWidget(title)
        
        self.level_label = QLabel("🎮 Nivel: ---")
        self.level_label.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        control_panel.addWidget(self.level_label)
        
        self.player_label = QLabel("👤 Jugador: ---")
        self.player_label.setFont(QFont('Arial', 12))
        control_panel.addWidget(self.player_label)
        
        self.coins_label = QLabel(f"💰 Monedas: {self.coins}")
        self.coins_label.setFont(QFont('Arial', 14))
        control_panel.addWidget(self.coins_label)
        
        self.score_label = QLabel(f"⭐ Puntos: {self.score}")
        self.score_label.setFont(QFont('Arial', 14))
        control_panel.addWidget(self.score_label)
        
        self.lives_label = QLabel(f"❤️ Vidas: {self.lives}")
        self.lives_label.setFont(QFont('Arial', 14))
        control_panel.addWidget(self.lives_label)
        
        self.wave_label = QLabel(f"🌊 Oleada: {self.wave}/{self.max_waves}")
        self.wave_label.setFont(QFont('Arial', 14))
        control_panel.addWidget(self.wave_label)
        
        control_panel.addWidget(QLabel("─" * 30))
        
        towers_label = QLabel("Selecciona Torre:")
        towers_label.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        control_panel.addWidget(towers_label)
        
        for rook_key, rook_data in ROOK_TYPES.items():
            btn = QPushButton(f"{rook_data['icon']} {rook_data['name']}\n💰 {rook_data['cost']} | ⚔️ {rook_data['damage']} | 📏 {rook_data['range']}")
            btn.setFixedHeight(60)
            btn.clicked.connect(lambda checked, key=rook_key: self.select_rook(key))
            control_panel.addWidget(btn)
        
        control_panel.addWidget(QLabel("─" * 30))
        
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
        
        info_label = QLabel("Menú → Juego → Nuevo Juego\npara comenzar\n\nClick derecho en torres\npara mejorarlas")
        info_label.setFont(QFont('Arial', 10))
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("color: #6b7280; padding: 10px;")
        control_panel.addWidget(info_label)
        
        main_layout.addLayout(control_panel)
        main_layout.setStretch(0, 3)
        main_layout.setStretch(1, 1)
    
    def select_rook(self, rook_key):
        self.selected_rook = rook_key
        QMessageBox.information(self, "Torre Seleccionada", 
                                f"Has seleccionado: {ROOK_TYPES[rook_key]['name']}")
    
    def cell_clicked(self, event, row, col):
        if not self.player_name:
            QMessageBox.warning(self, "Sin jugador", 
                               "Debes iniciar un nuevo juego desde el menú:\nJuego → Nuevo Juego")
            return
        
        # Click derecho para mejorar torre
        if event.button() == Qt.MouseButton.RightButton:
            cell = self.cells[row][col]
            if cell.content and cell.content['type'] == 'rook':
                rook = self.find_rook_at(row, col)
                if rook:
                    self.upgrade_rook(rook)
            return
        
        # Click izquierdo para colocar torre
        if not self.game_running:
            QMessageBox.warning(self, "Juego no iniciado", "Debes iniciar el juego primero")
            return
        
        cell = self.cells[row][col]
        
        if row == 0:
            QMessageBox.warning(self, "Posición inválida", "No puedes colocar torres en la zona crítica")
            return
        
        if cell.content is not None:
            QMessageBox.warning(self, "Posición ocupada", "Esta celda ya está ocupada")
            return
        
        rook_data = ROOK_TYPES[self.selected_rook]
        if self.coins < rook_data['cost']:
            QMessageBox.warning(self, "Monedas insuficientes", 
                                f"Necesitas {rook_data['cost']} monedas. Tienes: {self.coins}")
            return
        
        self.place_rook(row, col)
    
    def find_rook_at(self, row, col):
        """Encuentra la torre en una posición específica"""
        for rook in self.rooks:
            if rook.row == row and rook.col == col:
                return rook
        return None
    
    def upgrade_rook(self, rook):
        """Mejora una torre existente"""
        if not self.game_running:
            QMessageBox.warning(self, "Juego no iniciado", "Debes iniciar el juego primero")
            return
        
        dialog = UpgradeDialog(self, rook, self.coins)
        if dialog.exec():
            upgrade = dialog.get_upgrade()
            if upgrade:
                self.coins -= upgrade['cost']
                rook.upgrade(upgrade['type'])
                
                # Actualizar visualización
                self.cells[rook.row][rook.col].set_content(
                    'rook', 
                    rook.data,
                    f"Lv.{rook.upgrade_level}\n{rook.data['damage']}⚔️"
                )
                
                self.update_ui()
                QMessageBox.information(self, "Mejora exitosa", 
                                       f"Torre mejorada a nivel {rook.upgrade_level}")
    
    def place_rook(self, row, col):
        rook_data = ROOK_TYPES[self.selected_rook].copy()
        rook = Rook(self.selected_rook, row, col, self.next_rook_id)
        self.next_rook_id += 1
        
        self.rooks.append(rook)
        self.coins -= rook_data['cost']
        
        self.cells[row][col].set_content('rook', rook_data, f"Lv.1\n{rook_data['damage']}⚔️")
        self.update_ui()
    
    def start_game(self):
        if not self.player_name:
            QMessageBox.warning(self, "Sin jugador", 
                               "Debes iniciar un nuevo juego desde el menú:\nJuego → Nuevo Juego")
            return
            
        self.game_running = True
        self.start_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        
        # Obtener configuración del nivel
        level_config = LEVELS[self.current_level]
        
        self.game_timer.start(100)
        self.spawn_timer.start(level_config['spawn_interval'])
        self.move_timer.start(level_config['move_interval'])
    
    def pause_game(self):
        self.game_running = False
        self.game_timer.stop()
        self.spawn_timer.stop()
        self.move_timer.stop()
        self.start_btn.setEnabled(True)
        self.start_btn.setText("▶️ Continuar")
        self.pause_btn.setEnabled(False)
    
    def reset_game(self):
        self.game_running = False
        self.game_timer.stop()
        self.spawn_timer.stop()
        self.move_timer.stop()
        
        for row in self.cells:
            for cell in row:
                cell.clear_content()
        
        # Aplicar configuración del nivel
        self.apply_level_settings()
        
        self.score = 0
        self.wave = 1
        self.rooks = []
        self.avatars = []
        self.next_rook_id = 0
        self.next_avatar_id = 0
        self.avatars_spawned = 0
        
        self.start_btn.setText("▶️ Iniciar Juego")
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        
        self.update_ui()
    
    def spawn_avatar(self):
        if not self.game_running:
            return
        
        if self.avatars_spawned >= self.avatars_per_wave:
            if len(self.avatars) == 0:
                self.next_wave()
            return
        
        # Configuración del nivel para determinar tipos de enemigos
        level_config = LEVELS[self.current_level]
        boss_wave = level_config['boss_wave']
        
        # Aumentar dificultad con las oleadas
        if self.wave % boss_wave == 0 and random.random() < 0.4:
            avatar_type = 'BOSS'
        elif self.wave >= 3:
            avatar_type = random.choice(['BASIC', 'TANK', 'FAST', 'TANK'])
        else:
            avatar_type = random.choice(['BASIC', 'TANK', 'FAST'])
        
        col = random.randint(0, COLS - 1)
        
        if self.cells[ROWS - 1][col].content is None:
            avatar = Avatar(avatar_type, col, self.next_avatar_id)
            self.next_avatar_id += 1
            self.avatars.append(avatar)
            self.avatars_spawned += 1
            
            avatar_data = AVATAR_TYPES[avatar_type]
            hp_text = f"{avatar.hp}/{avatar.max_hp}"
            self.cells[ROWS - 1][col].set_content('avatar', avatar_data, hp_text)
    
    def next_wave(self):
        """Inicia la siguiente oleada"""
        if self.wave >= self.max_waves:
            self.level_completed()
            return
        
        self.wave += 1
        self.avatars_spawned = 0
        
        # Configuración del nivel
        level_config = LEVELS[self.current_level]
        base = level_config['avatars_per_wave_base']
        
        self.avatars_per_wave = base + (self.wave * 2)
        self.coins += 50 + (self.current_level * 25)  # Más bonus en niveles difíciles
        
        QMessageBox.information(self, "¡Nueva Oleada!", 
                               f"Oleada {self.wave}/{self.max_waves}\n"
                               f"+{50 + (self.current_level * 25)} monedas de bonus\n"
                               f"Enemigos: {self.avatars_per_wave}")
        self.update_ui()
    
    def level_completed(self):
        """Nivel completado exitosamente"""
        self.pause_game()
        
        bonus_score = 1000 * self.current_level
        self.score += bonus_score
        
        ScoreManager.save_score(self.player_name, self.score, self.wave, self.current_level)
        rank = ScoreManager.get_rank(self.score)
        
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("¡Nivel Completado!")
        msg.setText(f"¡Felicitaciones, {self.player_name}!")
        msg.setInformativeText(
            f"¡Has completado el Nivel {self.current_level}!\n\n"
            f"Puntuación: {self.score - bonus_score}\n"
            f"Bonus de nivel: +{bonus_score}\n"
            f"Puntuación final: {self.score}\n"
            f"Ranking: #{rank}\n\n"
            "Tu puntuación ha sido guardada."
        )
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        view_hof_btn = msg.addButton("Ver Hall of Fame", QMessageBox.ButtonRole.ActionRole)
        
        msg.exec()
        
        if msg.clickedButton() == view_hof_btn:
            self.show_hall_of_fame()
    
    def game_loop(self):
        if not self.game_running:
            return
        
        self.rooks_attack()
        self.update_ui()
        
        if self.lives <= 0:
            self.game_over()
    
    def move_avatars(self):
        """Mueve todos los avatares hacia arriba"""
        avatars_to_remove = []
        
        for avatar in self.avatars[:]:
            old_row = avatar.row
            old_col = avatar.col
            
            self.cells[old_row][old_col].clear_content()
            
            if not avatar.move_up():
                avatars_to_remove.append(avatar)
                self.lives -= 1
            else:
                avatar_data = AVATAR_TYPES[avatar.type]
                hp_text = f"{avatar.hp}/{avatar.max_hp}"
                self.cells[avatar.row][avatar.col].set_content('avatar', avatar_data, hp_text)
        
        for avatar in avatars_to_remove:
            if avatar in self.avatars:
                self.avatars.remove(avatar)
        
        self.update_ui()
    
    def rooks_attack(self):
        avatars_to_remove = []
        
        for rook in self.rooks:
            target = None
            min_distance = float('inf')
            
            for avatar in self.avatars:
                if rook.can_attack(avatar):
                    distance = abs(rook.row - avatar.row) + abs(rook.col - avatar.col)
                    if distance < min_distance:
                        min_distance = distance
                        target = avatar
            
            if target:
                if target.take_damage(rook.data['damage']):
                    avatars_to_remove.append(target)
                    self.coins += target.data['reward']
                    self.score += target.data['reward']
                    self.cells[target.row][target.col].clear_content()
                else:
                    avatar_data = AVATAR_TYPES[target.type]
                    hp_text = f"{target.hp}/{target.max_hp}"
                    self.cells[target.row][target.col].set_content('avatar', avatar_data, hp_text)
        
        for avatar in avatars_to_remove:
            if avatar in self.avatars:
                self.avatars.remove(avatar)
    
    def update_ui(self):
        if self.player_name:
            self.player_label.setText(f"👤 Jugador: {self.player_name}")
        
        level_config = LEVELS[self.current_level]
        level_color = level_config['color']
        self.level_label.setText(f"🎮 Nivel {self.current_level}: {level_config['name']}")
        self.level_label.setStyleSheet(f"color: {level_color}; font-weight: bold;")
        
        self.coins_label.setText(f"💰 Monedas: {self.coins}")
        self.score_label.setText(f"⭐ Puntos: {self.score}")
        self.lives_label.setText(f"❤️ Vidas: {self.lives}")
        self.wave_label.setText(f"🌊 Oleada: {self.wave}/{self.max_waves}")
    
    def game_over(self):
        """Termina el juego y guarda la puntuación"""
        self.pause_game()
        
        ScoreManager.save_score(self.player_name, self.score, self.wave, self.current_level)
        rank = ScoreManager.get_rank(self.score)
        
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Game Over")
        msg.setText(f"¡Juego terminado, {self.player_name}!")
        msg.setInformativeText(
            f"Nivel: {LEVELS[self.current_level]['name']}\n"
            f"Puntuación final: {self.score}\n"
            f"Oleada alcanzada: {self.wave}/{self.max_waves}\n"
            f"Ranking: #{rank}\n\n"
            f"Tu puntuación ha sido guardada en el Hall of Fame."
        )
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        view_hof_btn = msg.addButton("Ver Hall of Fame", QMessageBox.ButtonRole.ActionRole)
        
        msg.exec()
        
        if msg.clickedButton() == view_hof_btn:
            self.show_hall_of_fame()
    
    def closeEvent(self, event):
        """Detiene la música al cerrar"""
        self.music_player.stop()
        event.accept()

def main():
    app = QApplication(sys.argv)
    game = GameBoard()
    game.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()