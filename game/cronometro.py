import time

class Cronometro:
    def __init__(self):
        self._inicio = None
        self._acumulado = 0
        self._corriendo = False

    def iniciar(self):
        if not self._corriendo:
            self._inicio = time.time()
            self._corriendo = True

    def pausar(self):
        if self._corriendo:
            self._acumulado += time.time() - self._inicio
            self._corriendo = False

    def reiniciar(self):
        self._inicio = None
        self._acumulado = 0
        self._corriendo = False

    def tiempo(self):
        """Devuelve tiempo en segundos (float)."""
        if self._corriendo:
            return self._acumulado + (time.time() - self._inicio)
        return self._acumulado

    def tiempo_formateado(self):
        t = self.tiempo()
        minutos = int(t // 60)
        segundos = int(t % 60)
        milis   = int((t * 1000) % 1000)
        return f"{minutos:02d}:{segundos:02d}.{milis:03d}"
