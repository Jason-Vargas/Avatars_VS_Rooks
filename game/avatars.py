class Avatar:
    def __init__(self, fila, col, vida, ataque, vel_avance, vel_ataque, simbolo):
        self.fila = fila
        self.col = col
        self.vida = vida
        self.ataque = ataque
        self.vel_avance = vel_avance  # segundos
        self.vel_ataque = vel_ataque  # segundos
        self.simbolo = simbolo
        self.tiempo_desde_avance = 0
        self.tiempo_desde_ataque = 0
    
    def mover(self):
        """Avanza una columna hacia arriba (hacia la base)."""
        self.col -= 1

    def recibir_daño(self, dmg):
        self.vida -= dmg

    def esta_vivo(self):
        return self.vida > 0

    def puede_mover(self, dt):
        """dt = tiempo transcurrido real (en segundos)"""
        self.tiempo_desde_avance += dt
        if self.tiempo_desde_avance >= self.vel_avance:
            self.tiempo_desde_avance = 0
            return True
        return False

    def puede_atacar(self, dt):
        self.tiempo_desde_ataque += dt
        if self.tiempo_desde_ataque >= self.vel_ataque:
            self.tiempo_desde_ataque = 0
            return True
        return False


# -------------------------
# TIPOS DE AVATARES
# -------------------------

class Flechador(Avatar):
    def __init__(self, fila, col):
        super().__init__(
            fila, col,
            vida=5,
            ataque=2,
            vel_avance=12,
            vel_ataque=10,
            simbolo="🏹"
        )


class Escudero(Avatar):
    def __init__(self, fila, col):
        super().__init__(
            fila, col,
            vida=10,
            ataque=3,
            vel_avance=10,
            vel_ataque=15,
            simbolo="🛡️"
        )


class Leñador(Avatar):
    def __init__(self, fila, col):
        super().__init__(
            fila, col,
            vida=20,
            ataque=9,
            vel_avance=13,
            vel_ataque=5,
            simbolo="🪓"
        )


class Canibal(Avatar):
    def __init__(self, fila, col):
        super().__init__(
            fila, col,
            vida=25,
            ataque=12,
            vel_avance=14,
            vel_ataque=3,
            simbolo="🍖"
        )
