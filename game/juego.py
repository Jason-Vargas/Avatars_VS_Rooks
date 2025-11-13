import sys
from PyQt6.QtWidgets import QApplication
from tablero import Tablero

# Aquí importarás tus otras clases cuando las crees:
# from personajes import Personaje
# from enemigos import Enemigo

def main():
    """Función principal que ejecuta el juego"""
    app = QApplication(sys.argv)
    
    # Crear el tablero
    tablero = Tablero()
    tablero.show()
    
    # Aquí podrás crear e inicializar otros componentes:
    # personaje = Personaje()
    # enemigo = Enemigo()
    # tablero.actualizar_celda(0, 0, personaje.simbolo)
    
    # Ejemplo: actualizar algunas celdas
    tablero.actualizar_celda(0, 0, "🎮")
    tablero.actualizar_celda(4, 2, "☢")
    tablero.actualizar_celda(8, 4, "⚠️")
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()