# імпортуємо ситему сцен для меню
from scene import *
# імпортємо OpenGl для графіки
from OpenGL.GL import *
# імпортємо хітбокс для дебагу колайдерів
import hitbox
# імпортємо 'UserInterface' для намалювання меню і ид.
import ui
# імпортємо графіку для загрузки шейдерів
import graphics
# імпортємо час для вичислиння FPS
from engine.maths.time import *
# імпортємо вікно щоб його створити і на ньому малювати
from engine.graphics.window import *
# імпортємо 'інтернет' для зєдняня з сервером
from network.client import *

network = Network() # створюєм змінну для  зєдняня з сервером
WINDOW_TITLE = 'PyCraft' # створюєм змінну для назви вікна

if __name__ == '__main__':
    network.join(ServerInfo('localhost', 25565)) # зєднуємося з сервером по локольному серверу запортом 25565

    # Створюємо вікно і ставимо іконку для вікна
    Window.create(width=1280, height=720, title=WINDOW_TITLE, resizable=True)
    Window.set_icon('assets/icon.png')

    # Включаємо обв'язкові параметри для правилного рендеру
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glEnable(GL_BLEND)
    
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Завантажуємо шейдер світу, потрібні тільки вершинний та фрагментний (вершинний потрібен для перемноження на матриці перспективи, камери та моделі, а також для обчислення нормалей)
    # У грі є всього 2 шейдери - World (це шейдер для рендеру чанків) та Ui (це для кнопок, тексту та інших екранних елементів)
    hitbox.initialize() # для дебага
    ui.initialize() # підготовлюємо інтерфейс для роботи
    graphics.initialize() # підготовлюємо графіку для роботи

    time = Time() # створуємо екземплар класу для роботи з класом

    fps_timer = 0.0
    fps = 0

    Scene.set_scene(MainMenuScene())

    # Основний цикл вікна
    while Window.is_running():
        # Обновляємо вікно і чистимо буфера кольору та глибини (вона потрібна для OpenGL щоб він розумів який трикутник малювати спереду)    Window.update()
        Window.update()
        time.update()

        # створюєм змінні для облічення FPS
        fps_timer += time.get_delta()
        fps += 1

        if fps_timer >= 1.0:
            Window.set_title(f'{WINDOW_TITLE} | FPS: {fps}') # Пишим Кількість FPS

            # обнуляємо змінні для FPS
            fps_timer = 0.0
            fps = 0

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Чистим екран після останього кадру
        Scene.update_current() # обновлюємо сцени

    # Очищаємо всі об'єкти (шейдери, хітбокси і інше) 
    Scene.unload_current()

    hitbox.clear()
    ui.clear()
    graphics.clear()

    # Закриваєм вікно
    Window.close()