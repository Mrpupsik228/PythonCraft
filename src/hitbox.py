import glm

from engine.graphics.mesh import *
from maths.transform import Transform
from maths.camera import Camera
from engine.maths.util import *
from engine.graphics.shader import *

_mesh: Mesh
_shader: ShaderProgram

def initialize():
    global _mesh, _shader
    _mesh = Mesh(MeshBuffer([
        -0.5, -0.5, -0.5,
        0.5, -0.5, -0.5,
        0.5, -0.5, -0.5,
        0.5, -0.5, 0.5,
        0.5, -0.5, 0.5,
        -0.5, -0.5, 0.5,

        -0.5, 0.5, -0.5,
        0.5, 0.5, -0.5,
        0.5, 0.5, -0.5,
        0.5, 0.5, 0.5,
        0.5, 0.5, 0.5,
        -0.5, 0.5, 0.5,

        -0.5, -0.5, -0.5,
        -0.5, 0.5, -0.5,

        0.5, -0.5, -0.5,
        0.5, 0.5, -0.5,

        0.5, -0.5, 0.5,
        0.5, 0.5, 0.5,

        -0.5, -0.5, 0.5,
        -0.5, 0.5, 0.5
    ], 3), None, Mesh.LINES)

    _shader = ShaderProgram()
    _shader.load_shader(Shader.load_from_file('assets/shaders/hitbox.vert', Shader.VERTEX))
    _shader.load_shader(Shader.load_from_file('assets/shaders/hitbox.frag', Shader.FRAGMENT))
    _shader.compile()

    glLineWidth(2.5)

class RenderQueue:
    def __init__(self, transform: Transform, color: glm.vec3) -> None:
        self.transform = transform
        self.color = color

_render_queue: list[RenderQueue] = []

def render(transform: Transform, color: glm.vec3) -> None:
    _render_queue.append(RenderQueue(transform, color))

def render_all(fov: float, aspect: float, near: float, far: float, camera: Camera) -> None:
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glDisable(GL_CULL_FACE)

    _shader.load()
    _shader.set_uniform_mat4f('projection', glm.perspective(glm.radians(fov), aspect, near, far))
    _shader.set_uniform_mat4f('view', make_view_mat4(camera.position, camera.rotation))
    
    _mesh.load()
    
    for queue in _render_queue:
        _shader.set_uniform_mat4f('model', make_model_mat4(queue.transform.position, queue.transform.rotation, queue.transform.scale))
        _shader.set_uniform_3f('color', queue.color)

        _mesh.render()
    
    _render_queue.clear()

    _mesh.unload()
    _shader.unload()

    glEnable(GL_CULL_FACE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

def clear() -> None:
    _render_queue.clear()
    _mesh.unload()
    _shader.unload()