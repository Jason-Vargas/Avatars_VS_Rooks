from PySide6.QtCore import QTimer
import json
import os
from niveles_progresivos import NivelManager

class GameController:
    def __init__(self, tablero):
        self.tablero = tablero
        self.tablero.colocar_rook_callback = self.colocar_rook
        self.tablero.game_controller = self    
        self.avatars = []
        self.rooks = []
        self.monedas = []
        self.economia = 0
        self.game_over = False

        # Timer del juego (1 tick por segundo)
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(1000)  # 1 segundo por tick
        self.niveles_progresivos = NivelManager(self) # se debe colocar acá
        self.spawn_timer = QTimer()
        self.spawn_timer.timeout.connect(self.niveles_progresivos.spawn_avatar)
        self.coin_timer = QTimer()
        self.coin_timer.timeout.connect(self.spawn_coin)
        self.coin_timer.start(5000)

        # Niveles
        self.niveles_progresivos.iniciar_nivel()

        # Persistencia
        self.cargar_partida_si_corresponde()

        # Panel lateral
        self.actualizar_panel()

        # Cargar partida si existe
        self.actualizar_panel()

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
        # Verificar si completó el nivel
        if self.niveles_progresivos.oleada_actual >= self.niveles_progresivos.niveles[self.niveles_progresivos.nivel_actual]["oleadas"]:
            if len(self.avatars) == 0:  # No quedan avatars
                self.niveles_progresivos.completar_nivel()

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
                # Verificar si hay rook en la casilla hacia donde quiere avanzar
                destino_fila = avatar.fila - 1
                destino_col = avatar.col

                hay_rook = any(
                    r.fila == destino_fila and r.col == destino_col
                    for r in self.rooks
                )

                if not hay_rook:
                    # Mover
                    avatar.fila -= 1


    # --------------------------------------------
    # COMBATE ENTRE AVATARS Y ROOKS
    # --------------------------------------------
    def combate(self):
        for avatar in self.avatars:
            for rook in self.rooks:

                # Mismo número de columna
                if avatar.col == rook.col:

                    # Si el avatar está justo delante del rook
                    if avatar.fila == rook.fila + 1:

                        # Avatar ataca
                        if avatar.puede_atacar(1):
                            rook.recibir_daño(avatar.ataque)

                        # Rook ataca
                        if rook.puede_atacar(1):
                            avatar.recibir_daño(rook.ataque)
                            # Si el avatar muere → sumar economía
                            if not avatar.esta_vivo():
                                self.economia += 75
                                print(f"Avatar derrotado. Economía = {self.economia}")
                                self.actualizar_panel()

                                # quitar del tablero y de la lista
                                self.avatars.remove(avatar)
                                break    # salir del loop de rooks para evitar errores

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
        for moneda in self.monedas:
            self.tablero.actualizar_celda(moneda.fila, moneda.col, moneda.simbolo)

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

        for m in self.monedas:
            if m.fila == fila and m.col == col:
                print("No se puede poner una rook encima de una moneda.")
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
        
        if self.economia < nueva.costo:
            print(f"No tienes suficiente economía. Necesitas {nueva.costo}, tienes {self.economia}.")
            return

        self.economia -= nueva.costo
        print(f"Rook colocado. Economía restante: {self.economia}")
        self.actualizar_panel()

        # Añadir al juego
        self.rooks.append(nueva)
        self.tablero.actualizar_celda(fila, col, nueva.simbolo)

    def spawn_avatar(self):
        # Manejado por NivelManager
        pass

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

        # RESTAURAR economía
        self.economia = datos.get("economia", 0)

        # RESTAURAR NIVEL Y OLEADA
        self.niveles_progresivos.nivel_actual = datos.get("nivel_actual", 1)
        self.niveles_progresivos.oleada_actual = datos.get("oleada_actual", 1)
        self.tablero.mostrar_nivel(
            self.niveles_progresivos.niveles[self.niveles_progresivos.nivel_actual]["nombre"],
            self.niveles_progresivos.oleada_actual,
            self.niveles_progresivos.niveles[self.niveles_progresivos.nivel_actual]["oleadas"],
            self.niveles_progresivos.niveles[self.niveles_progresivos.nivel_actual]["color"]
        )

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
        self.actualizar_panel() 

    def guardar_partida(self, archivo="savegame.json"):
        print("DEBUG: iniciar guardado...")

        datos = {
            "economia": self.economia,
            "nivel_actual": self.niveles_progresivos.nivel_actual,
            "oleada_actual": self.niveles_progresivos.oleada_actual,
            "game_over": self.game_over,
            "avatars": [],
            "rooks": [],
            "monedas": []
        }

        # --- AVATARS ---
        for a in self.avatars:
            datos["avatars"].append({
                "tipo": type(a).__name__,
                "fila": a.fila,
                "col": a.col,
                "vida": a.vida
            })

        # --- ROOKS ---
        for r in self.rooks:
            datos["rooks"].append({
                "tipo": type(r).__name__,
                "fila": r.fila,
                "col": r.col,
                "vida": r.vida
            })

        # --- MONEDAS ---
        for m in self.monedas:
            datos["monedas"].append({
                "fila": m.fila,
                "col": m.col,
                "valor": m.valor
            })

        # Guardar archivo
        with open(archivo, "w") as f:
            json.dump(datos, f, indent=4)
        print(f"DEBUG: guardado en {archivo}")

        # meta
        with open("savegame_meta.json", "w") as f:
            json.dump({"safe_exit": True}, f)

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

    # monedas
    def spawn_coin(self):
        import random
        from moneda import Moneda

        # Obtener posiciones libres
        libres = []
        for f in range(self.tablero.filas):
            for c in range(self.tablero.columnas):
                # No puede existir avatar, rook ni moneda en esa celda
                ocupado_avatar = any(a.fila == f and a.col == c for a in self.avatars)
                ocupado_rook = any(r.fila == f and r.col == c for r in self.rooks)
                ocupado_moneda = any(m.fila == f and m.col == c for m in self.monedas)

                if not (ocupado_avatar or ocupado_rook or ocupado_moneda):
                    libres.append((f, c))

        if not libres:
            print("No hay espacio para monedas.")
            return

        fila, col = random.choice(libres)
        nueva = Moneda(fila, col)
        self.monedas.append(nueva)

        # Pintar en tablero
        self.tablero.actualizar_celda(fila, col, nueva.simbolo)
        print(f"Spawn MONEDA en ({fila}, {col}) valor={nueva.valor}")
    def recoger_moneda_en(self, fila, col):
        for m in self.monedas:
            if m.fila == fila and m.col == col:
                print(f"Moneda recogida en ({fila},{col}) +{m.valor}")

                # Sumar a economía
                self.economia += m.valor
                print(f"Economía total: {self.economia}")
                self.actualizar_panel()

                # Borrar visualmente
                self.tablero.actualizar_celda(fila, col, f"[{fila},{col}]")

                # Quitar de la lista
                self.monedas.remove(m)
                return  # Solo puede haber una moneda en esa celda

        print("No hay moneda en esta celda.")

    # Panel lateral
    def actualizar_panel(self):
        # Definir nombres y costos por tipo de rook
        rook_info = {
            1: ("Torre de Arena", 50),
            2: ("Torre de Piedra", 80),
            3: ("Torre de Fuego", 120),
            4: ("Torre de Agua", 150)
        }

        nombre, costo = rook_info.get(self.tablero.rook_seleccionada, ("-", 0))

        self.tablero.actualizar_panel(
            rook_name=nombre,
            costo=costo,
            economia=self.economia
        )