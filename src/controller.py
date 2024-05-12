from engine.graphics.window import *
from entity import LivingEntity
from maths.camera import *

def by_user(entity: LivingEntity) -> None:
    move_velocity = glm.vec2()

    if Window.is_key_pressed(pygame.K_w):
        move_velocity.x += glm.sin(glm.radians(entity.transform.rotation.y))
        move_velocity.y -= glm.cos(glm.radians(entity.transform.rotation.y))
        
    if Window.is_key_pressed(pygame.K_s):
        move_velocity.x += glm.sin(glm.radians(entity.transform.rotation.y + 180.0))
        move_velocity.y -= glm.cos(glm.radians(entity.transform.rotation.y + 180.0))
        
    if Window.is_key_pressed(pygame.K_d):
        move_velocity.x += glm.sin(glm.radians(entity.transform.rotation.y + 90.0))
        move_velocity.y -= glm.cos(glm.radians(entity.transform.rotation.y + 90.0))
        
    if Window.is_key_pressed(pygame.K_a):
        move_velocity.x += glm.sin(glm.radians(entity.transform.rotation.y - 90.0))
        move_velocity.y -= glm.cos(glm.radians(entity.transform.rotation.y - 90.0))
    
    move_velocity_length = glm.length(move_velocity)
    if move_velocity_length > 0.0:
        move_velocity = move_velocity / move_velocity_length * entity.speed
    
    entity.velocity.x = move_velocity.x
    entity.velocity.z = move_velocity.y

    if Window.is_key_pressed(pygame.K_SPACE):
        entity.jump(8.0 * 2.0)
    
    entity.transform.rotation.y += Window.get_mouse_velocity().x * 0.07
    entity.transform.rotation.x += Window.get_mouse_velocity().y * 0.07
    
    entity.transform.rotation.x = min(90, max(-90, entity.transform.rotation.x))
    entity.transform.rotation.y -= glm.floor(entity.transform.rotation.y / 360.0) * 360.0