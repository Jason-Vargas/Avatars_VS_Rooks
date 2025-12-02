import random

class Moneda:
    def __init__(self, fila, col):
        self.fila = fila
        self.col = col
        self.valor = random.choice([25, 50, 100])
        self.simbolo = f"💰{self.valor}"

    def __repr__(self):
        return f"Moneda({self.fila},{self.col}, valor={self.valor})"
