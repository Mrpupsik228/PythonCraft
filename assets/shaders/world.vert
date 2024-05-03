#version 410

layout(location=0) in vec3 position;
layout(location=1) in vec2 texcoord;
layout(location=2) in vec3 normal;

layout(location=0) out vec2 _texcoord;
layout(location=1) out vec3 _normal;
layout(location=2) out vec3 _position;

uniform mat4 projection, view, model;

void main() {
    vec4 modelPosition = model * vec4(position, 1.0);
    gl_Position = projection * view * modelPosition;

    _texcoord = vec2(texcoord.x, -texcoord.y);
    _normal = normalize((model * vec4(normal, 0.0)).xyz);
    _position = modelPosition.xyz;
}