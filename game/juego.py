import sys
from PySide6.QtWidgets import QApplication
from tablero import Tablero
from controlador import GameController
from avatars import Flechador, Escudero, Leñador, Canibal
from rooks import SandRook, RockRook, FireRook, WaterRook

def main():
    app = QApplication(sys.argv)

    tablero = Tablero()
    tablero.show()

    game = GameController(tablero)



    sys.exit(app.exec())

if __name__ == "__main__":
    main()