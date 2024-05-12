#version 410

layout(location=0) in vec3 position;
layout(location=1) in vec2 texcoord;
layout(location=2) in vec3 normal;

layout(location=0) out vec2 _texcoord;
layout(location=1) out vec3 _normal;

uniform mat4 projection, view, model;

void main() {
    gl_Position = projection * view * model * vec4(position, 1.0);

    _texcoord = vec2(texcoord.x, -texcoord.y);
    _normal = normalize((model * vec4(normal, 0.0)).xyz);
}