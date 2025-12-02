from PySide6.QtCore import QTimer
import json
import os
import sys

class GameController:
    def __init__(self, tablero):
        self.tablero = tablero
        self.tablero.colocar_rook_callback = self.colocar_rook
        self.tablero.game_controller = self    
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

        # Persistencia
        self.cargar_partida_si_corresponde()


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

    # Persistencia
    def cargar_partida_si_corresponde(self):
        meta_file = "savegame_meta.json"
        save_file = "savegame.json"
    
        if not os.path.exists(meta_file) or not os.path.exists(save_file):
            return
    
        with open(meta_file, "r") as f:
            meta = json.load(f)
    
        # Si la última salida fue segura → cargar partida
        if meta.get("safe_exit", False):
            print("Cargando partida previa...")
            self.cargar_partida()
    
        # IMPORTANTE: aquí marcamos automáticamente como salida NO segura
        # a menos que el usuario cierre con Escape.
        with open(meta_file, "w") as f:
            json.dump({"safe_exit": False}, f)

    def cargar_partida(self, archivo="savegame.json"):
        print(f"DEBUG: iniciar carga desde {archivo}")
        if not os.path.exists(archivo):
            print("DEBUG: archivo de guardado no existe.")
            return

        with open(archivo, "r") as f:
            try:
                datos = json.load(f)
            except Exception as e:
                print("ERROR leyendo savegame:", e)
                return

        # LIMPIAR ESTADO
        print("DEBUG: limpiando estado actual y tablero...")
        self.avatars = []
        self.rooks = []
        try:
            self.tablero.limpiar_tablero()
        except Exception as e:
            print("WARN: tablero no tiene limpiar_tablero() o falló:", e)

        # RECONSTRUIR AVATARS
        from avatars import Flechador, Escudero, Leñador, Canibal
        mapa_clases_avatars = {
            "Flechador": Flechador,
            "Escudero": Escudero,
            "Leñador": Leñador,
            "Canibal": Canibal
        }

        for a in datos.get("avatars", []):
            tipo = a.get("tipo")
            print("DEBUG: cargar avatar:", a)
            clase = mapa_clases_avatars.get(tipo)
            if clase:
                nuevo = clase(a["fila"], a["col"])
                if "vida" in a:
                    nuevo.vida = a["vida"]
                self.avatars.append(nuevo)
                self.tablero.actualizar_celda(nuevo.fila, nuevo.col, nuevo.simbolo)
            else:
                print(f"WARN: tipo avatar desconocido '{tipo}' - se omite")

        # RECONSTRUIR ROOKS
        from rooks import SandRook, RockRook, FireRook, WaterRook
        mapa_clases_rooks = {
            "SandRook": SandRook,
            "RockRook": RockRook,
            "FireRook": FireRook,
            "WaterRook": WaterRook
        }

        for r in datos.get("rooks", []):
            tipo = r.get("tipo")
            print("DEBUG: cargar rook:", r)
            clase = mapa_clases_rooks.get(tipo)
            if clase:
                nuevo = clase(r["fila"], r["col"])
                if "vida" in r:
                    nuevo.vida = r["vida"]
                self.rooks.append(nuevo)
                self.tablero.actualizar_celda(nuevo.fila, nuevo.col, nuevo.simbolo)
            else:
                print(f"WARN: tipo rook desconocido '{tipo}' - se omite")

        # RESTAURAR FLAGS
        self.game_over = datos.get("game_over", False)

        # REFRESCAR TABLERO (asegura que todo lo pintado quede consistente)
        try:
            self.refrescar_tablero()
        except Exception as e:
            print("WARN: refrescar_tablero falló:", e)

        print("DEBUG: carga completada. Avatars:", len(self.avatars), "Rooks:", len(self.rooks))

    def guardar_partida(self, archivo="savegame.json"):
        print("DEBUG: iniciar guardado...")
        datos = {
            "avatars": [],
            "rooks": [],
            "game_over": self.game_over
        }

        for a in self.avatars:
            datos["avatars"].append({
                "tipo": type(a).__name__,
                "fila": a.fila,
                "col": a.col,
                "vida": a.vida
            })

        for r in self.rooks:
            datos["rooks"].append({
                "tipo": type(r).__name__,
                "fila": r.fila,
                "col": r.col,
                "vida": r.vida
            })

        with open(archivo, "w") as f:
            json.dump(datos, f, indent=4)
        print(f"DEBUG: guardado en {archivo}")

        # marcar meta: la próxima vez cargar la partida
        meta = {"safe_exit": True}
        with open("savegame_meta.json", "w") as f:
            json.dump(meta, f)
        print("DEBUG: meta write load_on_start=True")

        print("Partida guardada. Cerrando juego...")
        self.salir_del_juego(called_from_save=True)

    def salir_del_juego(self, called_from_save=False):
        meta_file = "savegame_meta.json"
        # Si venimos de guardar (called_from_save=True) no sobreescribimos la meta
        if called_from_save:
            print("DEBUG: salir_del_juego() llamado desde guardar -> NO tocar meta")
        else:
            # escribir load_on_start = False porque cerramos normalmente
            print("DEBUG: marcar meta load_on_start=False por cierre normal")
            meta = {"load_on_start": False}
            with open(meta_file, "w") as f:
                json.dump(meta, f)

        # Cerrar la aplicación (PySide)
        print("DEBUG: sys.exit()")
        import sys
        sys.exit()
