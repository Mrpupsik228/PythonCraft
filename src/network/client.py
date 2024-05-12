import socket as sockets

class ServerInfo:
    def __init__(self, ip: str, port: int) -> None:
        self.ip = ip
        self.port = port

class Network:
    def __init__(self) -> None:
        self._socket = sockets.socket(sockets.AF_INET, sockets.SOCK_DGRAM)
        self.server_info: ServerInfo = None
    
    def join(self, server_info: ServerInfo) -> None:
        self.server_info = server_info
    def send_message(self, message: bytes) -> None:
        if self.server_info == None:
            print('ERROR: You\'re not connected to the server to send any messages! Use Network.join(server_info: ServerInfo) to join some')
            return
        
        self._socket.sendto(message, (self.server_info.ip, self.server_info.port))