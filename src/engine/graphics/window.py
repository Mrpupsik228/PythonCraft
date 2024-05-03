import pygame
import glm
from ctypes import windll
from OpenGL.GL import *

windll.user32.SetProcessDPIAware()
pygame.init()

class Window:
    # Дві приватні змінні: _surface - це саме поверхня дисплея, _running - допоміжна, щоб можна було вимкнути програму хрестиком
    _surface: pygame.Surface
    _running: False
    
    _keys: dict[int, int] = {}
    _buttons: dict[int, int] = {}

    _mouse_velocity = glm.vec2()
    _current_frame = 0

    @staticmethod
    def create(width: int, height: int, title: str, resizable: bool = True, vsync_enabled: bool = False) -> None:
        pygame.display.set_caption(title)
        pygame.display.set_mode((width, height), flags=pygame.OPENGL | pygame.DOUBLEBUF | (pygame.RESIZABLE if resizable else 0), vsync=(1 if vsync_enabled else 0))
        
        Window._running = True
        # Эта функция меняет цвет фона в OpenGL (RGBA), каналы от 0 до 1, то есть эти 4 значения дадут голубой цвет неба
        glClearColor(0.275, 0.62, 1.0, 1.0)
    
    @staticmethod
    def set_icon(location: str) -> None:
        pygame.display.set_icon(pygame.image.load(location))
    
    @staticmethod
    def set_mouse_grabbed(grabbed: bool) -> None:
        pygame.event.set_grab(grabbed)
        pygame.mouse.set_visible(not grabbed)

    # Базовое обновление окна PyGame
    @staticmethod
    def update() -> None:
        Window._current_frame += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Window._running = False
            elif event.type == pygame.KEYDOWN:
                Window._keys[event.key] = Window._current_frame
            elif event.type == pygame.KEYUP:
                Window._keys[event.key] = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                Window._buttons[event.button] = Window._current_frame
            elif event.type == pygame.MOUSEBUTTONUP:
                Window._buttons[event.button] = 0

        Window._mouse_velocity = pygame.mouse.get_rel()
        pygame.display.flip()
    
    # Закрытие окна PyGame и, на всякий случай, всего приложения, чтобы все потоки точно закрылись и все было ок
    @staticmethod
    def close() -> None:
        pygame.quit()
    
    @staticmethod
    def is_running() -> bool:
        return Window._running
    
    @staticmethod
    def get_width() -> int:
        return pygame.display.get_window_size()[0]
    @staticmethod
    def get_height() -> int:
        return pygame.display.get_window_size()[1]
    @staticmethod
    def get_size() -> glm.vec2:
        return glm.vec2(pygame.display.get_window_size())

    @staticmethod
    def is_key_pressed(key: int) -> bool:
        return key in Window._keys and Window._keys[key] != 0
    @staticmethod
    def is_key_just_pressed(key: int) -> bool:
        return key in Window._keys and Window._keys[key] == Window._current_frame

    @staticmethod
    def get_mouse_position() -> glm.vec2:
        return glm.vec2(pygame.mouse.get_pos())
    
    @staticmethod
    def get_mouse_velocity() -> glm.vec2:
        return glm.vec2(Window._mouse_velocity)

    @staticmethod
    def is_mouse_pressed(button: int) -> bool:
        return button in Window._buttons and Window._buttons[button] != 0
    
    @staticmethod
    def is_mouse_just_pressed(button: int) -> bool:
        return button in Window._buttons and Window._buttons[button] == Window._current_frame