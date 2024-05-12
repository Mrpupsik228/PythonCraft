import glm

class Transform:
    def __init__(self, position: glm.vec3, rotation: glm.vec3, scale: glm.vec3) -> None:
        self.position = glm.vec3(position)
        self.rotation = glm.vec3(rotation)
        self.scale = glm.vec3(scale)
    
    @staticmethod
    def clone(other):
        return Transform(other.position, other.rotation, other.scale)