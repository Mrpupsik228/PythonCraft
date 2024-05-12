from engine.graphics.mesh import Mesh, MeshBuffer
from engine.graphics.shader import ShaderProgram, Shader
from engine.graphics.window import Window
from engine.graphics.texture import Texture
from engine.maths.util import make_model_mat4
from OpenGL.GL import glDisable, glEnable, GL_DEPTH_TEST, GL_CULL_FACE
from maths.transform import *
from maths.util import *
from engine.sound import *


_square: Mesh
_shader: ShaderProgram

class Button:
    _buttons = []

    def __init__(self, position: glm.vec2, scale: float, texture: Texture) -> None:
        self.position = position
        self.scale = scale
        self.texture = texture
        self.sound = SoundSource()
        self.sound.set_sound('assets/sounds/aihk.wav')

        Button._buttons.append(self)
    
    def is_hovered(self) -> bool:
        scale = glm.vec2(self.scale) / 2.0
        
        aspect = self.texture.get_width() / self.texture.get_height()
        scale.x *= aspect

        return is_point_inside_area(convert_screen_to_ui(Window.get_mouse_position()), get_min(self.position, scale), get_max(self.position, scale))
    def is_pressed(self) -> bool:
        return self.is_hovered() and Window.is_mouse_pressed(0)
    def is_just_pressed(self) -> bool:
        if self.is_hovered() and Window.is_mouse_just_pressed(0):
            self.sound.play(False)
            return True
        else:
            return False
    
    def clear(self) -> None:
        Texture.clear(self.texture.get_id())
    def clear_all() -> None:
        for button in Button._buttons:
            button.clear()
        Button._buttons.clear()
    
    @staticmethod
    def render_all() -> None:
        for button in Button._buttons:
            aspect = button.texture.get_width() / button.texture.get_height()
            render(Transform(glm.vec3(button.position, 0.0), glm.vec3(), glm.vec3(aspect * button.scale, button.scale, 1.0)), button.texture.get_id())

def initialize() -> None:
    global _square, _shader
    
    _square = Mesh(MeshBuffer((-0.5,-0.5,0.5,-0.5,0.5,0.5,-0.5,0.5), 2), mode=Mesh.TRIANGLE_FAN)
    _shader = ShaderProgram()
    _shader.load_shader(Shader.load_from_file('assets/shaders/ui.vert', Shader.VERTEX))
    _shader.load_shader(Shader.load_from_file('assets/shaders/ui.frag', Shader.FRAGMENT))
    _shader.compile()

def begin() -> None:
    _shader.load()
    _shader.set_uniform_float('aspect', Window.get_width() / Window.get_height())
    _shader.set_uniform_integer('colorSampler', 0)
    
    _square.load()

    glDisable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)

def render(transform: Transform, texture: int | None = None) -> None:
    has_texture = texture != None
    if has_texture:
        Texture.load(0, texture)
    
    _shader.set_uniform_boolean('hasTexture', has_texture)
    _shader.set_uniform_mat4f('model', make_model_mat4(transform.position, transform.rotation, transform.scale))
    _square.render()

def end() -> None:
    _square.unload()
    _shader.unload()

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    
def clear() -> None:
    _square.clear()
    _shader.clear()