import glm

class Camera:
    def __init__(self, position: glm.vec3, rotation: glm.vec3) -> None:
        self.position = glm.vec3(position)
        self.rotation = glm.vec3(rotation)
    
    def teleport(self, position: glm.vec3, rotation: glm.vec3) -> None:
        self.position = glm.vec3(position)
        self.rotation = glm.vec3(rotation)