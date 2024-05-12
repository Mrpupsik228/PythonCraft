import graphics
import hitbox
import ui
import world
import controller
import random
import glm
from time import time as epoch_time
import pygame

from engine.maths import util as math_util
from engine.maths.time import *

from maths.transform import *
from entity import LivingEntity

from maths.camera import Camera

from engine.graphics.window import Window
from engine.graphics.texture import Texture

class Scene:
    _current = None

    def load(self) -> None:
        pass
    def update(self) -> None:
        pass
    def unload(self) -> None:
        pass

    @staticmethod
    def set_scene(scene) -> None:
        if Scene._current != None:
            Scene._current.unload()

        Scene._current = scene
        Scene._current.load()
    @staticmethod
    def update_current() -> None:
        if Scene._current != None:
            Scene._current.update()
    @staticmethod
    def unload_current() -> None:
        if Scene._current != None:
            Scene._current.unload()

class GameScene(Scene):
    def load(self) -> None:
        super().load()

        self.world_texture = Texture.load_from_file('assets/textures/terrain.png')
        self.camera = Camera(glm.vec3(), glm.vec3())

        self.chunk_meshes: dict[world.ChunkPos, world.ChunkMesh] = {}
        for chunk_pos in world.chunks.keys():
            self.chunk_meshes[chunk_pos] = world.ChunkMesh(world.chunks[chunk_pos])

        self.time = Time()
        self.player = LivingEntity(Transform(glm.vec3(20.5, 0.0, 20.5), glm.vec3(), glm.vec3(0.23, 0.86, 0.23))) # Коллайдеры от -1 до 1, так что высота складывается и вместо 1.72 метра получаем в два раза выше
        for i in range(world.Chunk.HEIGHT):
            if world.get_block(int(self.player.transform.position.x), int(glm.max(i - glm.ceil(self.player.transform.scale.y), 0)), int(self.player.transform.position.z)) == 0:
                self.player.transform.position.y = i - self.player.transform.scale.y * 0.5
                break
    
    def unload(self) -> None:
        super().unload()
        Texture.clear(self.world_texture.get_id())

        # Очищаємо всі об'єкти (шейдери, моделі тощо)
        for chunk_pos in self.chunk_meshes:
            self.chunk_meshes[chunk_pos].clear()
        self.chunk_meshes.clear()

        ui.Button.clear_all()

    def _render(self) -> None:
        fov = 90.0
        aspect = Window.get_width() / Window.get_height()
        near = 0.01
        far = 500.0

        # Завантажуємо шейдер світу та рендеримо всі чанки
        graphics.world_shader.load()
        graphics.world_shader.set_uniform_integer('colorSampler', 0)
        graphics.world_shader.set_uniform_mat4f('projection', glm.perspective(glm.radians(fov), aspect, near, far))
        graphics.world_shader.set_uniform_mat4f('view', math_util.make_view_mat4(self.camera.position, self.camera.rotation))

        Texture.load(0, self.world_texture.get_id())
        for chunk_pos in self.chunk_meshes.keys():
            graphics.world_shader.set_uniform_mat4f('model', math_util.make_model_mat4(glm.vec3(chunk_pos.x * world.Chunk.WIDTH, 0.0, chunk_pos.z * world.Chunk.LENGTH), glm.vec3(), glm.vec3(1.0)))

            chunk_mesh = self.chunk_meshes[chunk_pos]
            chunk_mesh.load()
            chunk_mesh.render()
            chunk_mesh.unload()

        Texture.unload()
        graphics.world_shader.unload()

        hitbox.render_all(fov, aspect, near, far, self.camera)
        
    def _update(self) -> None:
        self.player.update(self.time)
        controller.by_user(self.player)

        self.camera.teleport(
            glm.vec3(
                self.player.transform.position.x,
                self.player.transform.position.y + self.player.transform.scale.y - 0.05,
                self.player.transform.position.z
            ),
            self.player.transform.rotation
        )
    
    def update(self) -> None:
        super().update()
        self.time.update()
        
        if Window.is_key_just_pressed(pygame.K_ESCAPE):
            Window.set_mouse_grabbed(False)
            Scene.set_scene(MainMenuScene())
            
        elif Window.is_mouse_just_pressed(0):
            Window.set_mouse_grabbed(True)

        self._update()
        self._render()

class MainMenuScene(Scene):
    def load(self) -> None:
        super().load()
        
        MENU_BUTTONS_POSITION = glm.vec2(0.0, -0.25)
        MENU_BUTTONS_MARGIN = 0.025
        
        self.play_button = ui.Button(MENU_BUTTONS_POSITION + glm.vec2(0.0, 0.3 + MENU_BUTTONS_MARGIN), 0.3, Texture.load_from_file('assets/textures/button_play.png'))
        self.options_button = ui.Button(MENU_BUTTONS_POSITION, 0.3, Texture.load_from_file('assets/textures/button_options.png'))
        self.quit_button = ui.Button(MENU_BUTTONS_POSITION + glm.vec2(0.0, -0.3 - MENU_BUTTONS_MARGIN), 0.3, Texture.load_from_file('assets/textures/button_quit.png'))
        
        random.seed(epoch_time() * 3829.3024)
        
        self.title_textures = [
            Texture.load_from_file('assets/textures/title.png'),
            Texture.load_from_file('assets/textures/title2.png')
        ]

        self.random_title = random.randint(0, len(self.title_textures) - 1)
        
    def update(self) -> None:
        super().update()
        
        ui.begin()
        ui.Button.render_all()
        
        title_height = self.title_textures[self.random_title].get_height() / self.title_textures[self.random_title].get_width()
        
        ui.render(Transform(glm.vec3(0, 1 - title_height, 0), glm.vec3(), glm.vec3(1.5, title_height * 1.5, 1.0)), self.title_textures[self.random_title].get_id())
        ui.end()
        
        if self.options_button.is_just_pressed():
            Scene.set_scene(SoundMenu())
            
        if self.play_button.is_just_pressed():
            Scene.set_scene(GameScene())
            Window.set_mouse_grabbed(True)
        
        if self.quit_button.is_just_pressed():
            Window._running = False
        
    
    def unload(self) -> None:
        super().unload()

        for texture in self.title_textures:
            Texture.clear(texture.get_id())
        
        Texture.clear(self.play_button.texture.get_id())
        Texture.clear(self.options_button.texture.get_id())
        Texture.clear(self.quit_button.texture.get_id())

        ui.Button.clear_all()

class SoundMenu(Scene):
    def load(self) -> None:
        super().load()
        
        self.volume_index = 0
        self.volume_textures = [
            Texture.load_from_file('assets/textures/volume_off.png'),
            Texture.load_from_file('assets/textures/volume_25.png'),
            Texture.load_from_file('assets/textures/volume_50.png'),
            Texture.load_from_file('assets/textures/volume_100.png')
        ]
        self.volume_button = ui.Button(glm.vec2(0.0, 0.0), 0.4, self.volume_textures[self.volume_index])
        self.back_button = ui.Button(glm.vec2(-0.885, 0.8), 0.3, Texture.load_from_file("assets/textures/back_button.png"))

    def update(self) -> None:
        super().update()
        ui.begin()
        ui.Button.render_all()

        if self.volume_button.is_just_pressed():
            self.volume_index += 1
            if self.volume_index >= len(self.volume_textures):
                self.volume_index = 0
        
            self.volume_button.texture = self.volume_textures[self.volume_index]
        
        ui.end()
        
        if self.back_button.is_just_pressed():
            print("Volume")
            Scene.set_scene(MainMenuScene())
    
    def unload(self) -> None:
        super().unload()

        for texture in self.volume_textures:
            Texture.clear(texture.get_id())
        
        ui.Button.clear_all()