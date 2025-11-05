from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtGui import QPixmap, QPalette, QBrush
from PyQt6.QtCore import Qt
import os

class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("menu_dev/menu.ui", self)
        self.setWindowTitle("Menú principal")

        # Establecer imagen de fondo
        self.set_background()

        # Conectar botones
        self.btn_play.clicked.connect(self.start_game)
        self.btn_options.clicked.connect(self.open_options)
        self.btn_info.clicked.connect(self.open_info)
        self.btn_wiki.clicked.connect(self.open_wiki)
        self.btn_halloffame.clicked.connect(self.open_halloffame)
        self.btn_exit.clicked.connect(self.close)
        
        # Variables para mantener referencia a las ventanas
        self.game_window = None
        self.options_window = None
        self.info_window = None
        self.wiki_window = None
        self.halloffame_window = None
    
    def set_background(self):
        """Establece la imagen de fondo del menú"""
        # Construir la ruta a la imagen
        background_path = os.path.join("app", "images", "fondo2.jpg")
        
        try:
            # Cargar la imagen
            pixmap = QPixmap(background_path)
            
            if not pixmap.isNull():
                # Escalar la imagen al tamaño de la ventana
                scaled_pixmap = pixmap.scaled(
                    self.size(),
                    Qt.AspectRatioMode.IgnoreAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                
                # Crear la paleta y establecer el fondo
                palette = QPalette()
                palette.setBrush(QPalette.ColorRole.Window, QBrush(scaled_pixmap))
                self.setPalette(palette)
                
                print(f"🖼️ Fondo establecido: {background_path}")
            else:
                print(f"❌ No se pudo cargar la imagen: {background_path}")
                
        except Exception as e:
            print(f"❌ Error al establecer el fondo: {e}")
    
    def resizeEvent(self, event):
        """Se llama cuando la ventana cambia de tamaño"""
        super().resizeEvent(event)
        # Reescalar la imagen cuando cambia el tamaño de la ventana
        self.set_background()
    
    def start_game(self):
        """Inicia el juego abriendo GameBoard"""
        print("🎯 Iniciando juego…")
        
        try:
            # Importar aquí para evitar imports circulares
            from tools.Gameboard import GameBoard
            
            print("✅ GameBoard importado correctamente")
            
            # Crear y mostrar la ventana del juego
            self.game_window = GameBoard()
            print("✅ GameBoard creado")
            
            self.game_window.show()
            print("✅ GameBoard mostrado")
            
            # Cerrar el menú (opcional)
            self.close()
            
        except Exception as e:
            print(f"❌ Error al iniciar el juego: {e}")
            QMessageBox.critical(self, "Error", f"No se pudo iniciar el juego:\n{e}")
    
    def open_options(self):
        """Abre la ventana de opciones"""
        print("⚙️ Abriendo opciones…")
        
        try:
            # Importar la ventana de opciones (ajusta el import según tu estructura)
            from ventanas.optionWindow import OptionsWindow
            
            self.options_window = OptionsWindow()
            self.options_window.show()
            
        except Exception as e:
            print(f"❌ Error al abrir opciones: {e}")
            QMessageBox.critical(self, "Error", f"No se pudo abrir opciones:\n{e}")
    
    def open_info(self):
        """Abre la ventana de información"""
        print("ℹ️ Abriendo información…")
        
        try:
            # Importar desde la carpeta ventanas
            from ventanas.info import InfoWindow
            
            self.info_window = InfoWindow()
            self.info_window.show()
            
        except Exception as e:
            print(f"❌ Error al abrir información: {e}")
            QMessageBox.critical(self, "Error", f"No se pudo abrir información:\n{e}")
    
    def open_wiki(self):
        """Abre la ventana de wiki"""
        print("📖 Abriendo wiki…")
        
        try:
            # Importar desde la carpeta ventanas
            from ventanas.wiki import WikiWindow
            
            self.wiki_window = WikiWindow()
            self.wiki_window.show()
            
        except Exception as e:
            print(f"❌ Error al abrir wiki: {e}")
            QMessageBox.critical(self, "Error", f"No se pudo abrir wiki:\n{e}")
    
    def open_halloffame(self):
        """Abre la ventana de Hall of Fame"""
        print("🏆 Abriendo Hall of Fame…")
        
        try:
            # Importar desde la carpeta ventanas
            from ventanas.hallOfFame import HallOfFameWindow
            
            self.halloffame_window = HallOfFameWindow()
            self.halloffame_window.show()
            
        except Exception as e:
            print(f"❌ Error al abrir Hall of Fame: {e}")
            QMessageBox.critical(self, "Error", f"No se pudo abrir Hall of Fame:\n{e}")