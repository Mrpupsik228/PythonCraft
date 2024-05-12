# Імпортуємо необхідні бібліотеки двигуна
from scene import *
from OpenGL.GL import *

import hitbox
import ui
import graphics

from engine.maths.time import *
from engine.graphics.window import *

from network.client import *

WINDOW_TITLE = 'PyCraft'

if __name__ == '__main__':
    network = Network()
    network.join(ServerInfo('localhost', 25565))
    network.send_message(b'sldf')

    # Створюємо вікно з
    Window.create(width=1280, height=720, title=WINDOW_TITLE, resizable=True)
    Window.set_icon('assets/icon.png')

    # Включаємо перевірку на глибину
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glEnable(GL_BLEND)

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Завантажуємо шейдер світу, потрібні тільки вершинний та фрагментний (вершинний потрібен для перемноження на матриці перспективи, камери та моделі, а також для обчислення нормалей)
    # У грі є всього 2 шейдери - World (це шейдер для рендеру чанків) та Ui (це для кнопок, тексту та інших екранних елементів)
    hitbox.initialize()
    ui.initialize()
    graphics.initialize()

    time = Time()

    fps_timer = 0.0
    fps = 0

    Scene.set_scene(MainMenuScene())

    # Основний цикл вікна
    while Window.is_running():
        # Обновляємо вікно і чистимо буфера кольору та глибини (вона потрібна для OpenGL щоб він розумів який трикутник малювати спереду)    Window.update()
        Window.update()
        time.update()

        fps_timer += time.get_delta()
        fps += 1

        if fps_timer >= 1.0:
            Window.set_title(f'{WINDOW_TITLE} | FPS: {fps}')

            fps_timer = 0.0
            fps = 0

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Scene.update_current()

    # Очищаємо всі об'єкти (шейдери, моделі тощо) 
    Scene.unload_current()

    hitbox.clear()
    ui.clear()
    graphics.clear()

    # Закриваєм вікно
    Window.close()