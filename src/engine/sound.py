from pygame import mixer

mixer.init()
mixer.pause()

class SoundSource:
    def __init__(self) -> None:
        self._sound = None
    
    def set_sound(self, location: str) -> None:
        self._sound = mixer.Sound(location)
    
    def play(self, looping: bool) -> None:
        if self._sound != None:
            self._sound.play(1 if looping else 0)
    
    def set_volume(self, volume: float) -> None:
        if self._sound != None:
            self._sound.set_volume(volume)
    
    def stop(self) -> None:
        self.sound.stop()