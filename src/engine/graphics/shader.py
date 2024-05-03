from OpenGL.GL import *

# GLM - это удобная математическая библиотека, подходящая для работы с OpenGL
import glm

# Есть два класса - Shader и ShaderProgram.
# Shader - это отдельный шейдер в пайплайне OpenGL (Вершинный, геометрический или же фрагментный)
# ShaderProgram - это сборник всех шейдеров в одну большую программу, которую можно загрузить, отрисовать с ее помощью все модели и отгрузить

class Shader:
    # Удобная абстракция, чтобы вечно не писать GL_..._SHADER
    VERTEX = GL_VERTEX_SHADER
    FRAGMENT = GL_FRAGMENT_SHADER
    GEOMETRY = GL_GEOMETRY_SHADER

    # Конструктор, где создается и проверяется на ошибки код шейдера определенного типа
    def __init__(self, code: str, type: int) -> None:
        self._id = glCreateShader(type)
        
        # Загружаем код в шейдер и компилируем его
        glShaderSource(self._id, code)
        glCompileShader(self._id)

        # Проверяем на ошибки компиляции, если таковые имеются, крашим программу с выводом ошибки
        if glGetShaderiv(self._id, GL_COMPILE_STATUS) == GL_FALSE:
            raise Exception('Could not load shader:\n', glGetShaderInfoLog(self._id))
    
    def get_id(self) -> int:
        return self._id

    # Дополнительная статическая функция (статическая, так как она должна не являться частью экземпляра шейдера, а быть утилитой)
    # Она читает код с файла и создает на его основе шейдер
    @staticmethod
    def load_from_file(location: str, type: int):
        code: str
        with open(location, 'r') as file:
            code = '\n'.join(file.readlines())

        return Shader(code, type)

class ShaderProgram:
    def __init__(self) -> None:
        self._id = glCreateProgram()
        self._shaders: list[int] = []
        
    # Вигружає усі шейдери, видаляє їх і видаляє програму шейдерів (ні разі не вокористовуючи одні і ті самі шейдери в ріізних програмахб так що можна вибичити)
    def clear(self) -> None:
        for shader in self._shaders:
            glDetachShader(self._id, shader)
            glDeleteShader(shader)

            self._shaders.clear()
        
        glDeleteProgram(self._id)
    
    # Загружає шейдери
    def load_shader(self, shader: Shader) -> None:
        glAttachShader(self._id, shader.get_id())
        self._shaders.append(shader.get_id())
    
    def set_uniform_boolean(self, id: str, value: bool) -> None:
        glUniform1i(glGetUniformLocation(self._id, id), 1 if value else 0)
    def set_uniform_integer(self, id: str, value: int) -> None:
        glUniform1i(glGetUniformLocation(self._id, id), value)
    def set_uniform_float(self, id: str, value: float) -> None:
        glUniform1f(glGetUniformLocation(self._id, id), value)
    def set_uniform_2f(self, id: str, value) -> None:
        glUniform2f(glGetUniformLocation(self._id, id), value)
    def set_uniform_3f(self, id: str, value) -> None:
        glUniform3f(glGetUniformLocation(self._id, id), value)
    def set_uniform_4f(self, id: str, value) -> None:
        glUniform4f(glGetUniformLocation(self._id, id), value)
    def set_uniform_mat4f(self, id: str, value: glm.mat4) -> None:
        glUniformMatrix4fv(glGetUniformLocation(self._id, id), 1, GL_FALSE, value.to_list())
    
    # Компілює програму, в якій перед цем загрузили усі шейдери
    def compile(self):
        glLinkProgram(self._id)
        if glGetProgramiv(self._id, GL_LINK_STATUS) == GL_FALSE:
            raise Exception('Could not link program:\n', glGetProgramInfoLog(self._id))

        glValidateProgram(self._id)
        if glGetProgramiv(self._id, GL_VALIDATE_STATUS) == GL_FALSE:
            raise Exception('Could not validate program:\n', glGetProgramInfoLog(self._id))
    
    def load(self) -> None:
        glUseProgram(self._id)
    
    def get_id(self) -> int:
        return self._id
    
    # Статична Функція, так як її можна визвати від екземпляром програми, но вона не потрибує її (всі функції загрузки в OpenGL можна використовувити як функція відгрузки, замінивши id на 0, еквівалент до nullptr в С++)
    @staticmethod
    def unload() -> None:
        glUseProgram(0)