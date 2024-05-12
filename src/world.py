from engine.graphics.mesh import *
from perlin_noise import PerlinNoise
from random import randint
from sys import maxsize

import json
import random
import glm

gravity = 30.0

class Generator:
    _seed = randint(-1 - maxsize, maxsize)
    _noise = PerlinNoise(2, _seed)

    def get_height(x: float, z: float, scale: float) -> float:
        return min((Generator._noise([x / scale, z / scale]) / 2.0 + 0.5) * 20.0 + 4.0, Chunk.HEIGHT - 1.0)
    def get_block(x: float, y: float, z: float, height: float) -> int:
        ground_block = Blocks.GRASS[0]

        difference = int(height - y)
        if difference > 1:
            ground_block = Blocks.DIRT[0] if difference <= 2 else Blocks.STONE[0]

        return ground_block

class Chunk:
    WIDTH = 128
    HEIGHT = 64
    LENGTH = 128

    # Вместо обычного [] я использую bytearray([]), так как больше 256 типов блоков вряд-ли будет, а int весит в 4 раза больше, то есть 4-кратная (а то и больше) оптимизация для оперативки
    def __init__(self) -> None:
        self.blocks = bytearray([0] * Chunk.WIDTH * Chunk.HEIGHT * Chunk.LENGTH)

        # TODO: Заменить синус на отдельную функцию генерации мира
        for x in range(Chunk.WIDTH):
            for z in range(Chunk.LENGTH):
                height = Generator.get_height(x, z, 25.0)
                
                random.seed(x * 3294 + z * 9432)
                if random.random() < 0.005:
                    self.blocks[Chunk.get_xyz_index(x, int(height), z)] = Blocks.CHISELED_STONE[0]

                for y in range(int(height)):
                    self.blocks[Chunk.get_xyz_index(x, y, z)] = Generator.get_block(x, y, z, height)
                
    
    def get_block(self, x: int, y: int, z: int) -> int:
        return self.blocks[Chunk.get_xyz_index(x, y, z)]

    # Блоки хранятся как одномерный массив, поэтому нужна подобная функция, чтобы преобразовать удобный нам xyz в index блока
    def get_xyz_index(x: int, y: int, z: int) -> int:
        return x + z * Chunk.WIDTH + y * Chunk.WIDTH * Chunk.LENGTH
class ChunkPos:
    def __init__(self, x: int, z: int) -> None:
        self.x = x
        self.z = z
    
    def __eq__(self, other):
        if isinstance(other, ChunkPos):
            return self.x == other.x and self.z == other.z
        return False

    def __hash__(self):
        return hash((self.x, self.z))

class Block:
    FRONT = 0
    BACK = 1
    RIGHT = 2
    LEFT = 3
    TOP = 4
    BOTTOM = 5

    _blocks = []

    def __init__(self, id: str) -> None:
        self.uvs = [glm.vec4(0.9375, 0.9375, 0.0625, 0.0625)] * 6
        self._load_textures(f'assets/models/block/{id}.json')

        Block._blocks.append(self)
    
    def _load_textures(self, location):
        with open(location, 'r') as file:
            model = json.loads(file.read())
            textures = model['textures']
            
            if textures == None or not isinstance(textures, dict):
                return

            side: list[float] = self.uvs

            try:
                side = textures['all']
                if len(side) == 4:
                    for i in range(6):
                        self.uvs[i] = glm.vec4(side[0], side[1], side[2], side[3])
            except:
                pass
            
            try:
                side = textures['side']
                if len(side) == 4:
                    for i in range(4):
                        self.uvs[i] = glm.vec4(side[0], side[1], side[2], side[3])
            except:
                pass
            
            try:
                side = textures['top']
                if len(side) == 4:
                    self.uvs[Block.TOP] = glm.vec4(side[0], side[1], side[2], side[3])
            except:
                pass
            
            try:
                side = textures['bottom']
                if len(side) == 4:
                    self.uvs[Block.BOTTOM] = glm.vec4(side[0], side[1], side[2], side[3])
            except:
                pass
            
            try:
                side = textures['front']
                if len(side) == 4:
                    self.uvs[Block.FRONT] = glm.vec4(side[0], side[1], side[2], side[3])
            except:
                pass
            
            try:
                side = textures['back']
                if len(side) == 4:
                    self.uvs[Block.BACK] = glm.vec4(side[0], side[1], side[2], side[3])
            except:
                pass
            
            try:
                side = textures['left']
                if len(side) == 4:
                    self.uvs[Block.LEFT] = glm.vec4(side[0], side[1], side[2], side[3])
            except:
                pass
            
            try:
                side = textures['right']
                if len(side) == 4:
                    self.uvs[Block.RIGHT] = glm.vec4(side[0], side[1], side[2], side[3])
            except:
                pass
    
    def get_by_id(id: int):
        if id <= 0 or id > len(Block._blocks):
            return None
        
        return Block._blocks[id - 1]

class Blocks:
    DIRT = (1, Block('dirt'))
    GRASS = (2, Block('grass'))
    COBBLESTONE = (3, Block('cobblestone'))
    STONE = (4, Block('stone'))
    CHISELED_STONE = (5, Block('chiseled_stone'))

    @staticmethod
    def initialize() -> None:
        pass

Blocks.initialize()

class ChunkMesh(Mesh):
    '''
    Визуализация куба со всеми координатами вершин (x,y,z):
       0,1,0 +--------+ 1,1,0
            /|       /|
           / |      / |
    0,1,1 +--------+ 1|1,1
          |  |     |  |
       0,0|0 +-----|--+ 1,0,0
          | /      | /
          |/       |/
    0,0,1 +--------+ 1,0,1
    '''
    VERTICES = (
        # Передня сторона
        (
            0,0,1,
            1,0,1,
            0,1,1,
            0,1,1,
            1,0,1,
            1,1,1
        ),
        # Задня сторона
        (
            1,0,0,
            0,0,0,
            1,1,0,
            1,1,0,
            0,0,0,
            0,1,0
        ),
        # Правая сторона
        (
            1,0,1,
            1,0,0,
            1,1,1,
            1,1,1,
            1,0,0,
            1,1,0
        ),
        # Левая сторона
        (
            0,0,0,
            0,0,1,
            0,1,0,
            0,1,0,
            0,0,1,
            0,1,1
        ),
        # Верхняя сторона
        (
            0,1,1,
            1,1,1,
            0,1,0,
            0,1,0,
            1,1,1,
            1,1,0
        ),
        # Нижняя сторона
        (
            0,0,0,
            1,0,0,
            0,0,1,
            0,0,1,
            1,0,0,
            1,0,1
        )
    )
    # Тут всего одна штука, так как они идентичны на каждой стороне
    TEXCOORDS = (
        0,0,
        1,0,
        0,1,
        0,1,
        1,0,
        1,1
    )
    NORMALS = (
        (0,0,1),
        (0,0,-1),
        (1,0,0),
        (-1,0,0),
        (0,1,0),
        (0,-1,0)
    )

    def __init__(self, chunk: Chunk) -> None:
        # Подготавливаем списки для генерации меша
        vertices: list[float] = []
        texcoords: list[float] = []
        normals: list[float] = []

        for x in range(Chunk.WIDTH):
            for y in range(Chunk.HEIGHT):
                for z in range(Chunk.LENGTH):
                    center_block = chunk.get_block(x, y, z)
                    
                    # Если текущий блок воздух, то смысла генерировать стороны попросту нет
                    if center_block == 0:
                        continue

                    # Проходимся по каждой стороне куба (передняя, задняя, правая, левая, верхняя и нижняя) и если соседний блок воздух, то генерируем сторону
                    for i in range(6):
                        normal = ChunkMesh.NORMALS[i]
                        
                        next_x = x + normal[0]
                        next_y = y + normal[1]
                        next_z = z + normal[2]

                        if next_x < 0 or next_y < 0 or next_z < 0:
                            continue
                        if next_x >= Chunk.WIDTH or next_y >= Chunk.HEIGHT or next_z >= Chunk.LENGTH:
                            continue

                        # Для сдвига используются нормали, так как они как раз равны направлению для сдвига
                        if chunk.get_block(x + normal[0], y + normal[1], z + normal[2]) != 0:
                            continue

                        block = Block.get_by_id(center_block)
                        block_texcoords = list(ChunkMesh.TEXCOORDS)
                        for j in range(len(ChunkMesh.TEXCOORDS)):
                            block_texcoords[j] *= block.uvs[i].z if j % 2 == 0 else block.uvs[i].w
                            block_texcoords[j] += block.uvs[i].x if j % 2 == 0 else block.uvs[i].y

                        for j in range(len(ChunkMesh.VERTICES[i]) // 3):
                            vertices.append(ChunkMesh.VERTICES[i][j * 3] + x)
                            vertices.append(ChunkMesh.VERTICES[i][j * 3 + 1] + y)
                            vertices.append(ChunkMesh.VERTICES[i][j * 3 + 2] + z)
                        for texcoord in block_texcoords:
                            texcoords.append(texcoord)
                        for j in range(6):
                            for _normal in normal:
                                normals.append(_normal)

        super().__init__(MeshBuffer(vertices, 3), [MeshBuffer(texcoords, 2), MeshBuffer(normals, 3)], Mesh.TRIANGLES)

chunks: dict[ChunkPos, Chunk] = {}
chunks[ChunkPos(0, 0)] = Chunk()

def get_block(x: int, y: int, z: int) -> int:
    if y < 0 or y >= Chunk.HEIGHT:
        return 0

    chunk_x = x // Chunk.WIDTH
    chunk_z = z // Chunk.LENGTH

    chunk_pos = ChunkPos(chunk_x, chunk_z)
    
    if not (chunk_pos in chunks.keys()):
        return 0

    return chunks[chunk_pos].get_block(x - chunk_x * Chunk.WIDTH, y, z - chunk_z * Chunk.LENGTH)