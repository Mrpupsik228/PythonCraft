from math import sin, cos
from engine.graphics.mesh import *

gravity = 50.0

class Chunk:
    WIDTH = 256
    HEIGHT = 256
    LENGTH = 256

    # Вместо обычного [] я использую bytearray([]), так как больше 256 типов блоков вряд-ли будет, а int весит в 4 раза больше, то есть 4-кратная (а то и больше) оптимизация для оперативки
    def __init__(self) -> None:
        self.blocks = bytearray([0] * Chunk.WIDTH * Chunk.HEIGHT * Chunk.LENGTH)

        # TODO: Заменить синус на отдельную функцию генерации мира
        for x in range(Chunk.WIDTH):
            for z in range(Chunk.LENGTH):
                for y in range(int(((sin(x / 4.0) + cos(z / 4.0)) * 0.5 + 0.5) * 15.0)):
                    self.blocks[Chunk.get_xyz_index(x, y, z)] = 1
    
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
            1,1,0,
            1,1,1,
            1,0,0
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
        (
            0,0,1
        ),
        (
            0,0,-1
        ),
        (
            1,0,0
        ),
        (
            -1,0,0
        ),
        (
            0,1,0
        ),
        (
            0,-1,0
        )
    )

    # TODO: Добавить поддержку соседних чанков
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

                        for j in range(len(ChunkMesh.VERTICES[i]) // 3):
                            vertices.append(ChunkMesh.VERTICES[i][j * 3] + x)
                            vertices.append(ChunkMesh.VERTICES[i][j * 3 + 1] + y)
                            vertices.append(ChunkMesh.VERTICES[i][j * 3 + 2] + z)
                        for texcoord in ChunkMesh.TEXCOORDS:
                            texcoords.append(texcoord)
                        for j in range(6):
                            for _normal in normal:
                                normals.append(_normal)

        super().__init__(MeshBuffer(vertices, 3), [MeshBuffer(texcoords, 2), MeshBuffer(normals, 3)], Mesh.TRIANGLES)

chunks: dict[ChunkPos, Chunk] = {}
chunks[ChunkPos(0, 0)] = Chunk()