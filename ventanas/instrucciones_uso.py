from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                               QLabel, QPushButton, QTextEdit, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class InstruccionesUso(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Instrucciones de Uso")
        self.setFixedSize(600, 500)
        
        # IMPORTANTE: Inicializar la referencia de la ventana
        self.wiki_window = None
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Título
        titulo = QLabel("📖 Instrucciones del Juego")
        titulo.setFont(QFont("Arial", 18, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        # Texto de instrucciones
        instrucciones = QTextEdit()
        instrucciones.setReadOnly(True)
        instrucciones.setFont(QFont("Arial", 11))
        instrucciones.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                border: 2px solid #cccccc;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
        texto_instrucciones = """
<h3>🎮 Cómo Jugar</h3>

<p><b>Objetivo:</b> Protege la fuente de los malvados Avatars durante todas las oleadas.</p>

<p><b>Mecánica:</b></p>
<ul>
    <li>Al iniciar, tendrás un <b>monto económico preestablecido</b></li>
    <li>Usa tu dinero para <b>colocar Rooks estratégicamente</b> en el campo</li>
    <li>Los Rooks defenderán la fuente atacando a los Avatars que se acerquen</li>
    <li>Aguanta todas las oleadas para ganar</li>
</ul>

<p><b>Estrategia:</b> Posiciona los Rooks de forma inteligente para maximizar su efectividad y detener el avance enemigo.</p>

<p style="color: #666; font-style: italic;">💡 Tip: Cada Rook tiene habilidades únicas. ¡Úsalos sabiamente!</p>
        """
        
        instrucciones.setHtml(texto_instrucciones)
        layout.addWidget(instrucciones)
        
        # Botón para abrir wiki
        btn_wiki = QPushButton("📚 Conocer más sobre Avatars y Rooks")
        btn_wiki.setFont(QFont("Arial", 11, QFont.Bold))
        btn_wiki.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        btn_wiki.clicked.connect(self.abrir_wiki)
        layout.addWidget(btn_wiki)
        
        # Botón para cerrar
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setFont(QFont("Arial", 10))
        btn_cerrar.setStyleSheet("""
            QPushButton {
                background-color: #666666;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)
        btn_cerrar.clicked.connect(self.close)
        layout.addWidget(btn_cerrar)
    
    def abrir_wiki(self):
        """Abre la ventana de la wiki"""
        print("📚 Abriendo wiki desde opciones...")
        
        try:
            from ventanas.wiki import WikiWindow
            
            self.wiki_window = WikiWindow()
            self.wiki_window.show()
            print("✅ Wiki abierta correctamente")
            
        except ImportError as e:
            print(f"❌ Error de importación: {e}")
            QMessageBox.warning(
                self,
                "Archivo no encontrado",
                f"No se pudo cargar la wiki.\nError: {e}"
            )
        except Exception as e:
            print(f"❌ Error al abrir wiki: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo abrir la wiki:\n{e}"
            )