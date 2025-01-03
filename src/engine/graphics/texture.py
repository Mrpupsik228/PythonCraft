from OpenGL.GL import *
from pygame.image import load as pygame_image_load
from pygame.image import tostring as pygame_image_tostring

class Texture:
    def __init__(self, data: bytes, width: int, height: int) -> None:
        self._id = glGenTextures(1)
        
        glBindTexture(GL_TEXTURE_2D, self._id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        glGenerateMipmap(GL_TEXTURE_2D)

        self._width = width
        self._height = height
    
    def get_width(self) -> int:
        return self._width
    def get_height(self) -> int:
        return self._height
    def get_id(self) -> int:
        return self._id

    @staticmethod
    def load_from_file(location: str):
        image = pygame_image_load(location).convert_alpha()
        image_width, image_height = image.get_rect().size

        return Texture(pygame_image_tostring(image, 'RGBA'), image_width, image_height)
    
    # bank - это что-то типа номера текстуры, в который мы и загрузим ее, а уже в шейдере его можно будет получить, предварительно отправив по его названию set_uniform_integer('название', bank)
    @staticmethod
    def load(bank: int, texture: int) -> None:
        glActiveTexture(GL_TEXTURE0 + bank)
        glBindTexture(GL_TEXTURE_2D, texture)
    @staticmethod
    def unload() -> None:
        glBindTexture(GL_TEXTURE_2D, 0)
    @staticmethod
    def clear(texture: int) -> None:
        glDeleteTextures(1, (texture,))