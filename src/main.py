# Імпортуємо необхідні бібліотеки двигуна
from engine.graphics.window import *
from engine.graphics.mesh import *
from engine.graphics.texture import *
from engine.graphics.shader import *
from engine.math.time import *
from engine.math import util as math_util
from math import cos, sin
import world

# Створюємо вікно з
Window.create(width=1280, height=720, title='PyCraft', resizable=True)
Window.set_icon('assets/icon.png')
Window.set_mouse_grabbed(True)

# Включаємо перевірку на глибину
glEnable(GL_DEPTH_TEST)
glEnable(GL_CULL_FACE)

# Завантажуємо шейдер світу, потрібні тільки вершинний та фрагментний (вершинний потрібен для перемноження на матриці перспективи, камери та моделі, а також для обчислення нормалей)
# У грі є всього 2 шейдери - World (це шейдер для рендеру чанків) та Ui (це для кнопок, тексту та інших екранних елементів)
world_shader_program = ShaderProgram()
world_shader_program.load_shader(Shader.load_from_file('assets/shaders/world.vert', Shader.VERTEX))
world_shader_program.load_shader(Shader.load_from_file('assets/shaders/world.frag', Shader.FRAGMENT))
world_shader_program.compile()

chunk_meshes: dict[world.ChunkPos, world.ChunkMesh] = {}
for chunk_pos in world.chunks.keys():
    chunk_meshes[chunk_pos] = world.ChunkMesh(world.chunks[chunk_pos])

time = Time()

fps_timer = 0.0
fps = 0

camera_position = glm.vec3(20.0, 15.0, 20.0)
speed = 4.317
rotate_speed = 0.04

render_mode = False

camera_rotation = glm.vec3()

# Основний цикл вікна
while Window.is_running():
    # Обновляємо вікно і чистимо буфера кольору та глибини (вона потрібна для OpenGL щоб він розумів який трикутник малювати спереду)    Window.update()
    Window.update()
    time.update()

    fps_timer += time.get_delta()
    fps += 1

    if fps_timer >= 1.0:
        print(fps)

        fps_timer = 0.0
        fps = 0
    
    if Window.is_key_pressed(pygame.K_w):
        camera_position.x += speed * sin(glm.radians(camera_rotation.y)) * time.get_delta()
        camera_position.z -= speed * cos(glm.radians(camera_rotation.y)) * time.get_delta()
        
    if Window.is_key_pressed(pygame.K_s):
        camera_position.x += speed * sin(glm.radians(camera_rotation.y + 180.0)) * time.get_delta()
        camera_position.z -= speed * cos(glm.radians(camera_rotation.y + 180.0)) * time.get_delta()
        
    if Window.is_key_pressed(pygame.K_d):
        camera_position.x += speed * sin(glm.radians(camera_rotation.y + 90.0)) * time.get_delta()
        camera_position.z -= speed * cos(glm.radians(camera_rotation.y + 90.0)) * time.get_delta()
        
    if Window.is_key_pressed(pygame.K_a):
        camera_position.x += speed * sin(glm.radians(camera_rotation.y - 90.0)) * time.get_delta()
        camera_position.z -= speed * cos(glm.radians(camera_rotation.y - 90.0)) * time.get_delta()
        
    if Window.is_key_pressed(pygame.K_SPACE):
        camera_position.y += speed * time.get_delta()
        
    if Window.is_key_pressed(pygame.K_LSHIFT):
        camera_position.y -= speed * time.get_delta()
    
    camera_rotation.x = glm.clamp(camera_rotation.x + Window.get_mouse_velocity().y * rotate_speed, -90.0, 90.0)
    
    camera_rotation.y += Window.get_mouse_velocity().x * rotate_speed
    camera_rotation.y -= glm.floor(camera_rotation.y / 360.0) * 360.0
    
    if Window.is_key_just_pressed(pygame.K_F7):
        render_mode = not render_mode
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if render_mode else GL_FILL)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Завантажуємо шейдер світу та рендеримо всі чанки
    world_shader_program.load()
    world_shader_program.set_uniform_integer('colorSampler', 0)
    world_shader_program.set_uniform_mat4f('projection', glm.perspective(glm.radians(90.0), Window.get_width() / Window.get_height(), 0.01, 500.0))
    
    world_shader_program.set_uniform_mat4f('view', math_util.make_view_mat4(camera_position, camera_rotation))

    #Texture.load(0, texture)
    for chunk_pos in chunk_meshes.keys():
        world_shader_program.set_uniform_mat4f('model', math_util.make_model_mat4(glm.vec3(chunk_pos.x * world.Chunk.WIDTH, 0.0, chunk_pos.z * world.Chunk.LENGTH), glm.vec3(), glm.vec3(1.0)))

        chunk_mesh = chunk_meshes[chunk_pos]
        chunk_mesh.load()
        chunk_mesh.render()
        chunk_mesh.unload()

    #Texture.unload()

    world_shader_program.unload()

# Очищаємо всі об'єкти (шейдери, моделі тощо)
for chunk_mesh in chunk_meshes.values():
    chunk_mesh.clear()

world_shader_program.clear()

# Закриваєм вікно
Window.close()