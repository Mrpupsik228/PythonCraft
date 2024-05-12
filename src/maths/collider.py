from maths.transform import *

class Collider:
    def __init__(self, size: glm.vec3):
        self.size = size

    def get_min(self, transform: Transform) -> glm.vec3:
        return transform.position - transform.scale * self.size / 2.0
    
    def get_max(self, transform: Transform) -> glm.vec3:
        return transform.position + transform.scale * self.size / 2.0

    def get_extended(self, scale: glm.vec3):
        return Collider(self.size + scale)

    def clip_x(self, transform: Transform, other_transform: Transform, collider, velocity: float) -> float:
        min_a = self.get_min(transform)
        max_a = self.get_max(transform)

        min_b = collider.get_min(other_transform)
        max_b = collider.get_max(other_transform)

        if max_a.y <= min_b.y or min_a.y >= max_b.y:
            return velocity
        if max_a.z <= min_b.z or min_a.z >= max_b.z:
            return velocity

        if velocity < 0.0 and min_a.x >= max_b.x:
            _max = max_b.x - min_a.x
            if _max > velocity:
                velocity = _max
        if velocity > 0.0 and max_a.x <= min_b.x:
            _max = min_b.x - max_a.x
            if _max < velocity:
                velocity = _max

        return velocity
    
    def clip_y(self, transform: Transform, other_transform: Transform, collider, velocity: float) -> float:
        min_a = self.get_min(transform)
        max_a = self.get_max(transform)

        min_b = collider.get_min(other_transform)
        max_b = collider.get_max(other_transform)

        if max_a.x <= min_b.x or min_a.x >= max_b.x:
            return velocity

        if max_a.z <= min_b.z or min_a.z >= max_b.z:
            return velocity

        if velocity < 0.0 and min_a.y >= max_b.y:
            _max = max_b.y - min_a.y
            if _max > velocity:
                velocity = _max
    
        if velocity > 0.0 and max_a.y <= min_b.y:
            _max = min_b.y - max_a.y
            if _max < velocity:
                velocity = _max

        return velocity
    
    def clip_z(self, transform: Transform, other_transform: Transform, collider, velocity: float) -> float:
        min_a = self.get_min(transform)
        max_a = self.get_max(transform)

        min_b = collider.get_min(other_transform)
        max_b = collider.get_max(other_transform)

        if max_a.x <= min_b.x or min_a.x >= max_b.x:
            return velocity
        if max_a.y <= min_b.y or min_a.y >= max_b.y:
            return velocity

        if velocity < 0.0 and min_a.z >= max_b.z:
            _max = max_b.z - min_a.z
            if _max > velocity:
                velocity = _max
        if velocity > 0.0 and max_a.z <= min_b.z:
            _max = min_b.z - max_a.z
            if _max < velocity:
                velocity = _max

        return velocity