class Rook:
    def __init__(self, fila, col, vida, ataque, costo, simbolo):
        self.fila = fila
        self.col = col
        self.vida = vida
        self.ataque = ataque
        self.costo = costo
        self.simbolo = simbolo

        # Para ataques por tiempo
        self.tiempo_desde_ataque = 0
        self.vel_ataque = 3  # Puedes ajustarlo luego

    def recibir_daño(self, dmg):
        self.vida -= dmg

    def esta_vivo(self):
        return self.vida > 0

    def puede_atacar(self, dt):
        self.tiempo_desde_ataque += dt
        if self.tiempo_desde_ataque >= self.vel_ataque:
            self.tiempo_desde_ataque = 0
            return True
        return False


# -------------------------
# TIPOS DE ROOKS
# -------------------------

class SandRook(Rook):
    def __init__(self, fila, col):
        super().__init__(
            fila, col,
            vida=3,
            ataque=2,
            costo=50,
            simbolo="⛱️"
        )


class RockRook(Rook):
    def __init__(self, fila, col):
        super().__init__(
            fila, col,
            vida=14,
            ataque=4,
            costo=100,
            simbolo="🪨"
        )


class FireRook(Rook):
    def __init__(self, fila, col):
        super().__init__(
            fila, col,
            vida=16,
            ataque=8,
            costo=150,
            simbolo="🔥"
        )


class WaterRook(Rook):
    def __init__(self, fila, col):
        super().__init__(
            fila, col,
            vida=16,
            ataque=8,
            costo=150,
            simbolo="💧"
        )
