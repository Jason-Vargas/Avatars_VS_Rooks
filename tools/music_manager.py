import pygame


class MusicManager:
    def __init__(self):
        """Inicializa pygame mixer"""
        pygame.mixer.init()
        self._current_track = None
        self._volume = 0.7
        pygame.mixer.music.set_volume(self._volume)

    def play(self, track_path=None, loop=False):
        """
        Reproduce una pista de música
        
        Args:
            track_path: Ruta al archivo de música
            loop: Si True, reproduce en bucle infinito
        """
        if track_path:
            try:
                pygame.mixer.music.load(track_path)
                loops = -1 if loop else 0
                pygame.mixer.music.play(loops)
                self._current_track = track_path
                print(f"🎵 Reproduciendo: {track_path}")
            except Exception as e:
                print(f"❌ Error al reproducir música: {e}")
        elif self._current_track:
            # Si no se especifica track, reproduce el actual
            loops = -1 if loop else 0
            pygame.mixer.music.play(loops)

    def stop(self):
        """Detiene la música"""
        pygame.mixer.music.stop()
        print("⏹️ Música detenida")

    def pause(self):
        """Pausa la música"""
        pygame.mixer.music.pause()
        print("⏸️ Música pausada")

    def unpause(self):
        """Reanuda la música"""
        pygame.mixer.music.unpause()
        print("▶️ Música reanudada")

    def set_volume(self, volume):
        """
        Establece el volumen
        
        Args:
            volume: Valor entre 0.0 y 1.0
        """
        self._volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self._volume)

    def volume(self):
        """Retorna el volumen actual"""
        return self._volume

    def current_track(self):
        """Retorna la pista actual"""
        return self._current_track

    def is_playing(self):
        """Verifica si hay música reproduciéndose"""
        return pygame.mixer.music.get_busy()


# Instancia global del gestor de música
music = MusicManager()