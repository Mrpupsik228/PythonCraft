import glm
from engine.graphics.window import Window

def convert_screen_to_ui(coords: glm.vec2) -> glm.vec2:
    scaled = glm.vec2(coords.x / Window.get_width(), 1.0 - coords.y / Window.get_height()) * 2.0 - 1.0
    return scaled

def get_min(position: glm.vec2, size: glm.vec2) -> glm.vec2:
    return position - size / 2.0

def get_max(position: glm.vec2, size: glm.vec2) -> glm.vec2:
    return position + size / 2.0

def is_point_inside_area(point: glm.vec2, bounds_min: glm.vec2, bounds_max: glm.vec2) -> bool:
    return point.x > bounds_min.x and point.x < bounds_max.x and point.y > bounds_min.y and point.y < bounds_max.y