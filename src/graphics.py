from engine.graphics.shader import *

world_shader: ShaderProgram = None

def initialize() -> None:
    global world_shader, ui_shader

    world_shader = ShaderProgram()
    world_shader.load_shader(Shader.load_from_file('assets/shaders/world.vert', Shader.VERTEX))
    world_shader.load_shader(Shader.load_from_file('assets/shaders/world.frag', Shader.FRAGMENT))
    world_shader.compile()

    ui_shader = ShaderProgram()
    ui_shader.load_shader(Shader.load_from_file('assets/shaders/ui.vert', Shader.VERTEX))
    ui_shader.load_shader(Shader.load_from_file('assets/shaders/ui.frag', Shader.FRAGMENT))
    ui_shader.compile()
def clear() -> None:
    world_shader.clear()
    ui_shader.clear()