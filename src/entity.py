import world

from math.collider import *
from engine.math.time import *

class Entity:
    def __init__(self, transform: Transform, collider: Collider = Collider(glm.vec3(1.0))) -> None:
        self.transform = transform
        self.collider = collider

class LivingEntity(Entity):
    def __init__(self, transform: Transform, collider: Collider = Collider(glm.vec3(1.0))) -> None:
        super().__init__(transform, collider)
        
        self.velocity = glm.vec3()
        self.flying = False
    
    def update(self, time: Time) -> None:
        self.velocity.x = 0.0
        self.velocity.z = 0.0

        if not self.flying:
            self.velocity.y -= world.gravity * time.get_delta()
        else:
            self.velocity.y = 0.0
        
        # TODO: Implement collision detection with world and other entities
    
    def jump(self, height: float) -> None:
        self.velocity.y = height