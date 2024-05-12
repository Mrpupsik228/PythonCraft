import socket as sockets
from threading import Thread
from network.translator import *

class Server:
    def __init__(self) -> None:
        self._socket = sockets.socket(sockets.AF_INET, sockets.SOCK_DGRAM)
        self._thread = Thread(target=self._loop)
        self._running = False
    
    def _loop(self) -> None:
        while self._running:
            data, _ = self._socket.recvfrom(1024)
            print(f'New message: { Translator.read(data) }')
    def start(self, port: int) -> None:
        self._socket.bind((sockets.gethostbyname('localhost'), port))
        self._running = True
        self._thread.start()
    
    # Эта ебанная какашка с нихуя не работает!!!
    def stop(self) -> None:
        self._running = False
        self._thread.join()
        self._socket.shutdown(sockets.SHUT_RDWR)
        self._socket.close()
    
    def is_running(self) -> bool:
        return self._running