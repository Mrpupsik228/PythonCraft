from enum import Enum
from struct import unpack

class ReadMode(Enum):
    MOVE = 0
    SET_BLOCK = 1
    FIRE = 2

class MoveInfo:
    def __init__(self, x: float, y: float, z: float, angle: float) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.angle = angle

class SetBlockInfo:
    def __init__(self, id: int, x: int, y: int, z: int) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.z = z

class FireInfo:
    def __init__(self, dx: float, dy: float, dz: float) -> None:
        self.dx = dx
        self.dy = dy
        self.dz = dz

class Translator:
    def read(message: bytes) -> object:
        mode = ReadMode(ord(unpack('<c', bytes([message[0]]))[0]))
        data = bytes(message[1:])
        
        if mode == ReadMode.MOVE:
            if len(data) < 16:
                return
            
            splitted = unpack('<ffff', data)
            return MoveInfo(splitted[0], splitted[1], splitted[2], splitted[3])
        elif mode == ReadMode.SET_BLOCK:
            if len(data) < 13:
                return
            
            splitted = unpack('<ciii', data)
            return SetBlockInfo(ord(splitted[0]), splitted[1], splitted[2], splitted[3])
        elif mode == ReadMode.FIRE:
            if len(data) < 12:
                return
            
            splitted = unpack('<fff', data)
            return FireInfo(splitted[0], splitted[1], splitted[2])