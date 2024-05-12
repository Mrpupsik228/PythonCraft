#version 410

layout(location=0) in vec2 position;
layout(location=0) out vec2 _texcoord;

uniform float aspect;
uniform mat4 model;

void main() {
    gl_Position = model * vec4(position.x / aspect, position.y, 0.0, 1.0);
    _texcoord = position + 0.5;
    _texcoord.y *= -1.0;
}