from datetime import datetime, timedelta


class Cronometro:
    """
    Cronómetro para medir el tiempo que tarda un jugador en completar niveles.
    Soporta pausa/reanudar y guarda tiempos por nivel.
    """
    
    def __init__(self):
        self.start_time = None
        self.pause_time = None
        self.paused_duration = timedelta(0)
        self.is_running = False
        self.is_paused = False
        self.level_times = {}  # {nivel: tiempo_en_segundos}
        self.current_level = None
    
    def start(self, level=None):
        """Inicia el cronómetro"""
        if not self.is_running:
            self.start_time = datetime.now()
            self.paused_duration = timedelta(0)
            self.is_running = True
            self.is_paused = False
            self.current_level = level
            print(f"⏱️ Cronómetro iniciado{f' (Nivel {level})' if level else ''}")
        else:
            print("⚠️ El cronómetro ya está corriendo")
    
    def pause(self):
        """Pausa el cronómetro"""
        if self.is_running and not self.is_paused:
            self.pause_time = datetime.now()
            self.is_paused = True
            print("⏸️ Cronómetro pausado")
        else:
            print("⚠️ El cronómetro no está corriendo o ya está pausado")
    
    def resume(self):
        """Reanuda el cronómetro después de una pausa"""
        if self.is_running and self.is_paused:
            pause_duration = datetime.now() - self.pause_time
            self.paused_duration += pause_duration
            self.is_paused = False
            self.pause_time = None
            print("▶️ Cronómetro reanudado")
        else:
            print("⚠️ El cronómetro no está pausado")
    
    def stop(self, level=None):
        """
        Detiene el cronómetro y retorna el tiempo transcurrido en segundos.
        Si se proporciona un nivel, guarda el tiempo para ese nivel.
        """
        if not self.is_running:
            print("⚠️ El cronómetro no está corriendo")
            return 0
        
        # Si está pausado, calcular desde el momento de la pausa
        if self.is_paused:
            end_time = self.pause_time
        else:
            end_time = datetime.now()
        
        # Calcular tiempo total
        elapsed = end_time - self.start_time - self.paused_duration
        total_seconds = int(elapsed.total_seconds())
        
        # Guardar tiempo del nivel
        level_id = level or self.current_level
        if level_id is not None:
            self.level_times[level_id] = total_seconds
            print(f"⏹️ Nivel {level_id} completado en: {self.format_time(total_seconds)}")
        
        # Resetear estado
        self.is_running = False
        self.is_paused = False
        self.start_time = None
        self.pause_time = None
        self.paused_duration = timedelta(0)
        
        return total_seconds
    
    def get_elapsed_time(self):
        """
        Obtiene el tiempo transcurrido sin detener el cronómetro.
        Retorna el tiempo en segundos.
        """
        if not self.is_running:
            return 0
        
        if self.is_paused:
            end_time = self.pause_time
        else:
            end_time = datetime.now()
        
        elapsed = end_time - self.start_time - self.paused_duration
        return int(elapsed.total_seconds())
    
    def get_total_time(self):
        """Retorna el tiempo total de todos los niveles completados"""
        return sum(self.level_times.values())
    
    def get_level_time(self, level):
        """Retorna el tiempo de un nivel específico"""
        return self.level_times.get(level, 0)
    
    def reset(self):
        """Reinicia completamente el cronómetro"""
        self.start_time = None
        self.pause_time = None
        self.paused_duration = timedelta(0)
        self.is_running = False
        self.is_paused = False
        self.level_times = {}
        self.current_level = None
        print("🔄 Cronómetro reiniciado")
    
    @staticmethod
    def format_time(seconds):
        """
        Formatea segundos a formato HH:MM:SS o MM:SS
        Args:
            seconds (int): Tiempo en segundos
        Returns:
            str: Tiempo formateado
        """
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    @staticmethod
    def format_time_compact(seconds):
        """
        Formatea tiempo de forma compacta (ej: 1h 23m 45s)
        Args:
            seconds (int): Tiempo en segundos
        Returns:
            str: Tiempo formateado
        """
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        parts = []
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        if secs > 0 or not parts:
            parts.append(f"{secs}s")
        
        return " ".join(parts)
    
    def get_statistics(self):
        """Retorna un diccionario con estadísticas del cronómetro"""
        return {
            "total_time": self.get_total_time(),
            "total_time_formatted": self.format_time(self.get_total_time()),
            "levels_completed": len(self.level_times),
            "level_times": self.level_times.copy(),
            "is_running": self.is_running,
            "is_paused": self.is_paused,
            "current_elapsed": self.get_elapsed_time() if self.is_running else 0
        }
    
    def __str__(self):
        """Representación en string del cronómetro"""
        if self.is_running:
            status = "PAUSADO" if self.is_paused else "CORRIENDO"
            elapsed = self.get_elapsed_time()
            return f"Cronómetro [{status}] - Tiempo: {self.format_time(elapsed)}"
        else:
            total = self.get_total_time()
            return f"Cronómetro [DETENIDO] - Tiempo total: {self.format_time(total)}"
