from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QPushButton, QLabel, QSlider, QCheckBox, QComboBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from tools.music_manager import MusicManager
import os


class OptionsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.music = MusicManager()
        self.setWindowTitle("⚙️ Opciones")
        self.setMinimumSize(500, 500)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Título
        title = QLabel("Configuración")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Selector de música de fondo
        music_layout = QHBoxLayout()
        music_label = QLabel("🎼 Música de fondo:")
        music_label.setStyleSheet("font-size: 14px;")
        self.music_combo = QComboBox()
        self.music_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #999;
                border-radius: 5px;
                font-size: 13px;
            }
        """)
        
        # Cargar canciones disponibles
        self.load_available_music()
        self.music_combo.currentIndexChanged.connect(self.on_music_changed)
        
        music_layout.addWidget(music_label)
        music_layout.addWidget(self.music_combo)
        music_layout.addStretch()
        main_layout.addLayout(music_layout)
        
        # Sección de volumen
        volume_layout = QVBoxLayout()
        volume_label = QLabel("🔊 Volumen de música:")
        volume_label.setStyleSheet("font-size: 14px;")
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(int(self.music.volume() * 100))
        self.volume_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #999;
                height: 8px;
                background: #ddd;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #5b9bd5;
                border: 1px solid #5b9bd5;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
        """)
        self.volume_value = QLabel(f"{int(self.music.volume() * 100)}%")
        self.volume_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.volume_slider.valueChanged.connect(self.update_volume_label)
        
        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(self.volume_slider)
        volume_layout.addWidget(self.volume_value)
        main_layout.addLayout(volume_layout)
        
        # Sección de efectos de sonido
        sfx_layout = QVBoxLayout()
        sfx_label = QLabel("🎵 Volumen de efectos:")
        sfx_label.setStyleSheet("font-size: 14px;")
        self.sfx_slider = QSlider(Qt.Orientation.Horizontal)
        self.sfx_slider.setMinimum(0)
        self.sfx_slider.setMaximum(100)
        self.sfx_slider.setValue(80)
        self.sfx_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #999;
                height: 8px;
                background: #ddd;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #70ad47;
                border: 1px solid #70ad47;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
        """)
        self.sfx_value = QLabel("80%")
        self.sfx_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sfx_slider.valueChanged.connect(self.update_sfx_label)
        
        sfx_layout.addWidget(sfx_label)
        sfx_layout.addWidget(self.sfx_slider)
        sfx_layout.addWidget(self.sfx_value)
        main_layout.addLayout(sfx_layout)
        
        # Checkbox de pantalla completa
        self.fullscreen_check = QCheckBox("🖥️  Pantalla completa")
        self.fullscreen_check.setStyleSheet("font-size: 14px;")
        main_layout.addWidget(self.fullscreen_check)
        
        # Selector de dificultad
        difficulty_layout = QHBoxLayout()
        difficulty_label = QLabel("🎯 Dificultad:")
        difficulty_label.setStyleSheet("font-size: 14px;")
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Fácil", "Normal", "Difícil", "Experto"])
        self.difficulty_combo.setCurrentIndex(1)
        self.difficulty_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #999;
                border-radius: 5px;
                font-size: 13px;
            }
        """)
        
        difficulty_layout.addWidget(difficulty_label)
        difficulty_layout.addWidget(self.difficulty_combo)
        difficulty_layout.addStretch()
        main_layout.addLayout(difficulty_layout)
        
        main_layout.addStretch()
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        self.btn_apply = QPushButton("✅ Aplicar")
        self.btn_apply.setMinimumHeight(40)
        self.btn_apply.setStyleSheet("""
            QPushButton {
                background-color: #70ad47;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a8c38;
            }
        """)
        self.btn_apply.clicked.connect(self.apply_settings)
        
        self.btn_cancel = QPushButton("❌ Cancelar")
        self.btn_cancel.setMinimumHeight(40)
        self.btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #c44e4e;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #a03d3d;
            }
        """)
        self.btn_cancel.clicked.connect(self.close)
        
        buttons_layout.addWidget(self.btn_apply)
        buttons_layout.addWidget(self.btn_cancel)
        main_layout.addLayout(buttons_layout)
        
        # Cargar configuración actual
        self.load_current_settings()
    
    def load_available_music(self):
        """Carga las canciones disponibles de la carpeta soundtrack"""
        self.music_combo.addItem("(Sin música)", None)
        
        soundtrack_path = "soundtrack"
        if os.path.exists(soundtrack_path):
            music_files = [f for f in os.listdir(soundtrack_path) 
                          if f.endswith(('.mp3', '.wav', '.ogg'))]
            
            for music_file in sorted(music_files):
                # Mostrar nombre sin extensión
                display_name = os.path.splitext(music_file)[0].title()
                # Guardar ruta completa como dato
                full_path = os.path.join(soundtrack_path, music_file)
                self.music_combo.addItem(display_name, full_path)
    
    def load_current_settings(self):
        """Carga la configuración actual del music_manager"""
        # Cargar música actual
        current_music = self.music.current_track()
        if current_music:
            for i in range(self.music_combo.count()):
                if self.music_combo.itemData(i) == current_music:
                    self.music_combo.setCurrentIndex(i)
                    break
    
    def on_music_changed(self, index):
        """Se llama cuando cambia la selección de música"""
        music_path = self.music_combo.itemData(index)
        if music_path:
            self.music.play(music_path, loop=True)
        else:
            self.music.stop()
    
    def update_volume_label(self, value):
        """Actualiza la etiqueta del volumen de música"""
        self.volume_value.setText(f"{value}%")
        # Actualizar volumen en tiempo real
        self.music.set_volume(value / 100.0)
    
    def update_sfx_label(self, value):
        """Actualiza la etiqueta del volumen de efectos"""
        self.sfx_value.setText(f"{value}%")
    
    def apply_settings(self):
        """Aplica la configuración"""
        print("✅ Configuración aplicada:")
        print(f"   - Música: {self.music_combo.currentText()}")
        print(f"   - Volumen música: {self.volume_slider.value()}%")
        print(f"   - Volumen efectos: {self.sfx_slider.value()}%")
        print(f"   - Pantalla completa: {self.fullscreen_check.isChecked()}")
        print(f"   - Dificultad: {self.difficulty_combo.currentText()}")
        
        # Aplicar la música seleccionada
        music_path = self.music_combo.itemData(self.music_combo.currentIndex())
        if music_path:
            self.music.play(music_path, loop=True)
        else:
            self.music.stop()
        
        self.music.set_volume(self.volume_slider.value() / 100.0)
        
        self.close()