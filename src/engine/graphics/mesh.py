# numpy честно не нужен, просто почему-то без него OpenGL не хочет воспринимать массивы вершин, поэтому достал только функцию array и тип данных float32 (То есть обычный float - 4 байта)
from numpy import array, float32
from OpenGL.GL import *

# Это Pojo класс, который просто имеет в себе вершины и количество измерений (x, xy, xyz или же, если быть богом - xyzw)
class MeshBuffer:
    def __init__(self, data: tuple[float], dimensions: int) -> None:
        self.data = array(data, dtype=float32)
        self.dimensions = dimensions

# Это основной класс Mesh, он нужен чтобы легко создать модель со всеми вершинами и ее отрендерить :)
class Mesh:
    # Абстракция (чисто для удобства), это режимы сбора вершин в полигоны
    TRIANGLES = GL_TRIANGLES
    TRIANGLE_FAN = GL_TRIANGLE_FAN
    TRIANGLE_STRIP = GL_TRIANGLE_STRIP
    LINES = GL_LINES
    LINE_STRIP = GL_LINE_STRIP
    LINE_LOOP = GL_LINE_LOOP
    POINTS = GL_POINTS

    # Конструктор, в котором просто создаются vao (можно сказать, это список из vbo) и все vbo (это как списки чисел, в нашем случае вершин)
    def __init__(self, vertices: MeshBuffer, additional: list[MeshBuffer] = None, mode: int = TRIANGLES) -> None:
        self.mode = mode # На место mode надо пихать Mesh.РЕЖИМ_РЕНДЕРА (TRIANGLES, TRIANGLE_FAN, TRIANGLE_STRIP или же LINES)
        
        # Вычисляем количество vbo и создаем массив на этой основе
        additional_count = 0 if additional == None else len(additional)
        self.buffers = [None] * (1 + additional_count)

        # Создаем сам vao
        self.vao = glGenVertexArrays(1)
        self.load()

        # Создаем основной и дополнительные vbo
        self._create_vbo(vertices, 0)
        for i in range(additional_count):
            self._create_vbo(additional[i], i + 1)

        # Вычисляем количество вершин (нужно для glDrawArrays(), чтобы объяснить сколько вершин рисовать) и отгружаем модель, чтобы другие безопасно загружались, не перезаписывая эту
        self.vertex_count = len(vertices.data) // vertices.dimensions
        self.unload()
    
    # Удобная функция для создания vbo (нижнее подчеркивание используется чтобы показать, что функция / переменная приватная и не должны быть доступны из других классов)
    def _create_vbo(self, buffer: MeshBuffer, index: int) -> None:
        self.buffers[index] = glGenBuffers(1)

        glBindBuffer(GL_ARRAY_BUFFER, self.buffers[index])
        glBufferData(GL_ARRAY_BUFFER, buffer.data.nbytes, buffer.data, GL_STATIC_DRAW) # Умножаем на 4, так как 4 - это размер float в байтах, а OpenGL требует именно в них

        glVertexAttribPointer(index, buffer.dimensions, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
        glEnableVertexAttribArray(index)

    # Эти функции говорят сами за себя, загружаем, рендерим (разделение на три функции нужно, так как одну и ту же модель можно рисовать несколько раз) и отгружаем
    def load(self) -> None:
        glBindVertexArray(self.vao)
        
    def render(self) -> None:
        glDrawArrays(self.mode, 0, self.vertex_count)
        
    def unload(self) -> None:
        glBindVertexArray(0)
    
    # Очистка всех vao и vbo очень важны, особенно в бесконечном мире майнкрафта, где каждую секунду создаются новые чанки, а старые пропадают!
    def clear(self) -> None:
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(len(self.buffers), self.buffers)