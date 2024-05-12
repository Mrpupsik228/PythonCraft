#version 410

layout(location=0) in vec3 position;
uniform mat4 projection, view, model;

void main() {
    gl_Position = projection * view * model * vec4(position, 1.0);
}