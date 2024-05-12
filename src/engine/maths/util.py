import glm

def make_view_mat4(position: glm.vec3, rotation: glm.vec3) -> glm.mat4:
    matrix = glm.mat4()
    matrix = glm.rotate(matrix, glm.radians(rotation.x), glm.vec3(1.0, 0.0, 0.0))
    matrix = glm.rotate(matrix, glm.radians(rotation.y), glm.vec3(0.0, 1.0, 0.0))
    matrix = glm.rotate(matrix, glm.radians(rotation.z), glm.vec3(0.0, 0.0, 1.0))
    matrix = glm.translate(matrix, -position)

    return matrix

def make_model_mat4(position: glm.vec3, rotation: glm.vec3, scale: glm.vec3) -> glm.mat4:
    matrix = glm.mat4()
    matrix = glm.translate(matrix, position)
    matrix = glm.rotate(matrix, glm.radians(rotation.x), glm.vec3(1.0, 0.0, 0.0))
    matrix = glm.rotate(matrix, glm.radians(rotation.y), glm.vec3(0.0, 1.0, 0.0))
    matrix = glm.rotate(matrix, glm.radians(rotation.z), glm.vec3(0.0, 0.0, 1.0))
    matrix = glm.scale(matrix, scale)

    return matrix