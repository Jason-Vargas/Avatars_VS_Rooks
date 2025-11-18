from PySide6.QtCore import QTimer


class GameController:
    def __init__(self, tablero):
        self.tablero = tablero
        self.tablero.colocar_rook_callback = self.colocar_rook
        self.avatars = []
        self.rooks = []
        self.game_over = False

        # Timer del juego (1 tick por segundo)
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(1000)  # 1 segundo por tick
        self.spawn_timer = QTimer()
        self.spawn_timer.timeout.connect(self.spawn_avatar)
        self.spawn_timer.start(10000)  # cada 10 segundos


    # --------------------------------------------
    # REGISTRO DE ENTIDADES
    # --------------------------------------------
    def agregar_avatar(self, avatar):
        self.avatars.append(avatar)
        self.tablero.actualizar_celda(avatar.fila, avatar.col, avatar.simbolo)

    def agregar_rook(self, rook):
        self.rooks.append(rook)
        self.tablero.actualizar_celda(rook.fila, rook.col, rook.simbolo)

    # --------------------------------------------
    # TICK DEL JUEGO
    # --------------------------------------------
    def tick(self):
        if self.game_over:
            return

        self.mover_avatars()
        self.combate()
        self.limpiar_muertos()
        self.refrescar_tablero()

    # --------------------------------------------
    # MOVIMIENTO DE AVATARS
    # --------------------------------------------
    def mover_avatars(self):
        for avatar in self.avatars:

            # Si un avatar llega a la fila roja → game over
            if avatar.fila == 0:
                self.game_over = True
                self.tablero.actualizar_celda(0, 0, "💀GAME OVER💀")
                self.timer.stop()
                return

            # Movimiento si cooldown lo permite
            if avatar.puede_mover(1):
                avatar.fila -= 1   # ¡Ahora hacia arriba!


    # --------------------------------------------
    # COMBATE ENTRE AVATARS Y ROOKS
    # --------------------------------------------
    def combate(self):
        for avatar in self.avatars:
            for rook in self.rooks:

                # Mismo número de fila
                if avatar.fila == rook.fila:

                    # Si el avatar está justo delante del rook
                    if avatar.col == rook.col + 1:

                        # Avatar ataca
                        if avatar.puede_atacar(1):
                            rook.recibir_daño(avatar.ataque)

                        # Rook ataca
                        if rook.puede_atacar(1):
                            avatar.recibir_daño(rook.ataque)

    # --------------------------------------------
    # ELIMINAR ENTIDADES MUERTAS
    # --------------------------------------------
    def limpiar_muertos(self):
        self.avatars = [a for a in self.avatars if a.esta_vivo()]
        self.rooks = [r for r in self.rooks if r.esta_vivo()]

    # --------------------------------------------
    # ACTUALIZAR VISUAL DEL TABLERO
    # --------------------------------------------
    def refrescar_tablero(self):
        # Limpiar todas las celdas menos la fila roja
        for f in range(1, self.tablero.filas):
            for c in range(self.tablero.columnas):
                self.tablero.actualizar_celda(f, c, f"[{f},{c}]")

        # Mostrar avatars
        for avatar in self.avatars:
            self.tablero.actualizar_celda(avatar.fila, avatar.col, avatar.simbolo)

        # Mostrar rooks
        for rook in self.rooks:
            self.tablero.actualizar_celda(rook.fila, rook.col, rook.simbolo)
    def colocar_rook(self, fila, col, tipo):
        # Verificar colisiones
        for r in self.rooks:
            if r.fila == fila and r.col == col:
                print("Ya hay una rook ahí.")
                return

        for a in self.avatars:
            if a.fila == fila and a.col == col:
                print("No se puede poner una rook encima de un avatar.")
                return

        # Importar clases
        from rooks import SandRook, RockRook, FireRook, WaterRook

        # Seleccionar tipo
        if tipo == 1:
            nueva = SandRook(fila, col)
        elif tipo == 2:
            nueva = RockRook(fila, col)
        elif tipo == 3:
            nueva = FireRook(fila, col)
        elif tipo == 4:
            nueva = WaterRook(fila, col)
        else:
            print("Tipo inválido")
            return

        # Añadir al juego
        self.rooks.append(nueva)
        self.tablero.actualizar_celda(fila, col, nueva.simbolo)
    def spawn_avatar(self):
        import random
        from avatars import Flechador, Escudero, Leñador, Canibal

        col = random.randint(0, self.tablero.columnas - 1)
        fila = self.tablero.filas - 1  # última fila

        nuevo = Flechador(fila, col)
        self.avatars.append(nuevo)
        self.tablero.actualizar_celda(fila, col, nuevo.simbolo)
        print(f"Spawn avatar en ({fila}, {col})")
        nuevo = Escudero(fila,col)
        self.avatars.append(nuevo)
        self.tablero.actualizar_celda(fila, col, nuevo.simbolo)
        print(f"Spawn avatar en ({fila}, {col})")
        nuevo = Leñador(fila,col)
        self.avatars.append(nuevo)
        self.tablero.actualizar_celda(fila, col, nuevo.simbolo)
        print(f"Spawn avatar en ({fila}, {col})")
        nuevo = Canibal(fila,col)
        self.avatars.append(nuevo)
        self.tablero.actualizar_celda(fila, col, nuevo.simbolo)
        print(f"Spawn avatar en ({fila}, {col})")
