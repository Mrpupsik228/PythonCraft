# функция time из библиотеки time нужна для получения текущего времени с момента "Epoch" (переименовал в timer, чтобы избежать конфликтов и путаницы)
from time import time as timer

class Time:
    def __init__(self) -> None:
        # scale - это переменная, отвечающая за скорость времени, очень удобно когда надо протестировать что-либо "в замедленной съемке"
        self.scale = 1.0

        self._delta = 0.0
        self._time = 0.0
        self._last_time = 0.0

        # Функция update здесь вызывается воизбежания мгновенного очень большого числа равного значению timer
        self.update()
    
    # Нужно вызывать каждый кадр при выполнении программы, чтобы вычеслить delta time (промежуток в секундах между каждым кадром) и время с момента создания экземпляра класса Time
    def update(self) -> None:
        current_time = timer()
        
        self._delta = (current_time - self._last_time) * self.scale
        self._last_time = current_time

        self._time += self._delta
    
    def get_delta(self) -> float:
        return self._delta