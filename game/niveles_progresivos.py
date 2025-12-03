import random
from avatars import Flechador, Escudero, Leñador, Canibal

class NivelManager:
    def __init__(self, controlador):
        self.controlador = controlador
        self.nivel_actual = 1
        self.oleada_actual = 0
        self.max_niveles = 3
        
        # Configuración de niveles
        self.niveles = {
            1: {
                "nombre": "🌱 NIVEL 1 - PRINCIPIANTE",
                "oleadas": 5,
                "spawn_interval": 10000,  # 10 segundos
                "economia_inicial": 300,
                "avatars_por_oleada": 2,
                "tipos_avatars": [Flechador, Escudero],
                "color": "#4CAF50"
            },
            2: {
                "nombre": "⚔️ NIVEL 2 - INTERMEDIO",
                "oleadas": 7,
                "spawn_interval": 8000,  # 8 segundos
                "economia_inicial": 250,
                "avatars_por_oleada": 3,
                "tipos_avatars": [Flechador, Escudero, Leñador],
                "color": "#FF9800"
            },
            3: {
                "nombre": "🔥 NIVEL 3 - EXPERTO",
                "oleadas": 10,
                "spawn_interval": 6000,  # 6 segundos
                "economia_inicial": 200,
                "avatars_por_oleada": 4,
                "tipos_avatars": [Flechador, Escudero, Leñador, Canibal],
                "color": "#F44336"
            }
        }
    def iniciar_nivel(self):
        """Inicia el nivel actual"""
        config = self.niveles[self.nivel_actual]
        self.oleada_actual = 0

        # Configurar economía inicial
        self.controlador.economia = config["economia_inicial"]

        # Configurar intervalo del spawn
        self.controlador.spawn_timer.setInterval(config["spawn_interval"])

        # Limpiar estado de listas
        self.controlador.avatars = []
        self.controlador.rooks = []
        self.controlador.monedas = []
        self.controlador.game_over = False

        # Actualizar UI
        self.controlador.tablero.mostrar_nivel(
            config["nombre"],
            self.oleada_actual,
            config["oleadas"],
            config["color"]
        )
        self.controlador.actualizar_panel()

        print(f"🎮 {config['nombre']} iniciado")
        print(f"💰 Economía inicial: {config['economia_inicial']}")
        print(f"📊 Oleadas totales: {config['oleadas']}")
        self.controlador.spawn_timer.start()

    def spawn_avatar(self):
        print("🚨 spawn_avatar llamado")
        """Genera avatars según el nivel actual"""
        if self.controlador.game_over:
            print("Spawn cancelado: game over")
            return

        config = self.niveles[self.nivel_actual]
        self.controlador.spawn_timer.setInterval(config["spawn_interval"])

        # Verificar si aún quedan oleadas
        if self.oleada_actual >= config["oleadas"]:
            print("No más oleadas; completando nivel...")
            self.completar_nivel()
            return

        # AVANZAR oleada
        self.oleada_actual += 1

        print(f"🌊 Oleada {self.oleada_actual}/{config['oleadas']}")

        # Actualizar UI
        self.controlador.tablero.actualizar_oleada(
            self.oleada_actual, config["oleadas"]
        )

        # Variables necesarias
        num_avatars = config["avatars_por_oleada"]
        tipos_disponibles = config["tipos_avatars"]

        # GENERAR AVATARS
        for _ in range(num_avatars):

            col = random.randint(0, self.controlador.tablero.columnas - 1)
            fila = self.controlador.tablero.filas - 1

            tipo_avatar = random.choice(tipos_disponibles)
            nuevo = tipo_avatar(fila, col)

            self.controlador.agregar_avatar(nuevo)
            self.controlador.refrescar_tablero()

            print(f"  └─ Spawn {tipo_avatar.__name__} en ({fila}, {col})")

    
    def completar_nivel(self):
        """Se ejecuta cuando se completan todas las oleadas"""
        # Verificar si quedan avatars vivos
        if len(self.controlador.avatars) > 0:
            print("⏳ Esperando a que se eliminen todos los avatars...")
            return
        
        config = self.niveles[self.nivel_actual]
        print(f"✅ {config['nombre']} COMPLETADO!")
        
        # Detener spawns
        self.controlador.spawn_timer.stop()
        
        # Verificar si es el último nivel
        if self.nivel_actual >= self.max_niveles:
            self.victoria_total()
        else:
            self.pasar_siguiente_nivel()
    
    def pasar_siguiente_nivel(self):
        """Avanza al siguiente nivel"""
        self.nivel_actual += 1
        
        # Mostrar pantalla de transición
        self.controlador.tablero.mostrar_transicion_nivel(
            self.nivel_actual,
            self.niveles[self.nivel_actual]["nombre"]
        )
        
        # Dar bonus de economía
        bonus = 200
        self.controlador.economia += bonus
        print(f"💰 Bonus de nivel: +{bonus} oro")
        
        # Esperar 5 segundos antes de iniciar el siguiente nivel
        from PySide6.QtCore import QTimer
        QTimer.singleShot(5000, self.iniciar_nivel)
    
    def victoria_total(self):
        """Se ejecuta cuando se completan todos los niveles"""
        print("🏆 ¡VICTORIA TOTAL! ¡HAS COMPLETADO TODOS LOS NIVELES!")
        
        self.controlador.timer.stop()
        self.controlador.coin_timer.stop()
        
        # Mostrar pantalla de victoria
        self.controlador.tablero.mostrar_victoria()
        
        # Agregar al Hall of Fame
        try:
            from ventanas.hallOfFame import HallOfFameWindow
            # Aquí necesitarías obtener el username del jugador
            # Por ahora usaremos un placeholder
            HallOfFameWindow.add_winner("Jugador")
        except Exception as e:
            print(f"⚠️ No se pudo agregar al Hall of Fame: {e}")
    
    def obtener_progreso(self):
        """Retorna el progreso actual"""
        return {
            "nivel": self.nivel_actual,
            "oleada": self.oleada_actual,
            "oleadas_totales": self.niveles[self.nivel_actual]["oleadas"],
            "nombre_nivel": self.niveles[self.nivel_actual]["nombre"]
        }