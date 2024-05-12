import world
import hitbox

from maths.collider import *
from engine.maths.time import *

class Entity:
    def __init__(self, transform: Transform, collider: Collider = Collider(glm.vec3(1.0))) -> None:
        self.transform = transform
        self.collider = collider

        self.velocity = glm.vec3()
    
    def update(self, time: Time) -> None:
        self.transform.position += self.velocity * time.get_delta()

class LivingEntity(Entity):
    def __init__(self, transform: Transform, collider: Collider = Collider(glm.vec3(1.0))) -> None:
        super().__init__(transform, collider)
        self.speed = 4.317

        self.on_ground = False
        self.flying = False
    
    def update(self, time: Time) -> None:
        self.velocity.y -= 0.0 if self.flying else world.gravity * time.get_delta()
        
        # TODO: Implement collision detection with world and other entities
        scaled_velocity = self.velocity * time.get_delta()

        extended_collider = self.collider.get_extended(glm.abs(scaled_velocity))
        min = extended_collider.get_min(self.transform)
        max = extended_collider.get_max(self.transform)

        range_x = range(int(glm.floor(min.x) - 1), int(glm.ceil(max.x) + 1))
        range_y = range(int(glm.floor(min.y) - 1), int(glm.ceil(max.y) + 1))
        range_z = range(int(glm.floor(min.z) - 1), int(glm.ceil(max.z) + 1))
        
        block_collider = Collider(glm.vec3(1.0))
        last_velocity_y = scaled_velocity.y

        for x in range_x:
            for y in range_y:
                for z in range_z:
                    block = world.get_block(x, y, z)

                    if block != 0:
                        block_transform = Transform(glm.vec3(x, y, z) + 0.5, glm.vec3(), glm.vec3(1.0))
                        scaled_velocity.x = self.collider.clip_x(self.transform, block_transform, block_collider, scaled_velocity.x)
        self.transform.position.x += scaled_velocity.x

        for x in range_x:
            for y in range_y:
                for z in range_z:
                    block = world.get_block(x, y, z)

                    if block != 0:
                        block_transform = Transform(glm.vec3(x, y, z) + 0.5, glm.vec3(), glm.vec3(1.0))
                        scaled_velocity.z = self.collider.clip_z(self.transform, block_transform, block_collider, scaled_velocity.z)
        self.transform.position.z += scaled_velocity.z

        for x in range_x:
            for y in range_y:
                for z in range_z:
                    block = world.get_block(x, y, z)

                    if block != 0:
                        block_transform = Transform(glm.vec3(x, y, z) + 0.5, glm.vec3(), glm.vec3(1.0))
                        scaled_velocity.y = self.collider.clip_y(self.transform, block_transform, block_collider, scaled_velocity.y)
        self.transform.position.y += scaled_velocity.y

        self.on_ground = False
        if last_velocity_y != scaled_velocity.y and last_velocity_y < 0.0:
            self.velocity.y = 0.0
            self.on_ground = True
            
    def jump(self, height: float) -> None:
        if self.on_ground:
            self.velocity.y = height
            self.on_ground = False