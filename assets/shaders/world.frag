#version 410
#define SUN_DIRECTION normalize(vec3(0.3, 1.0, 0.6))
#define AMBIENT 0.3

layout(location=0) in vec2 _texcoord;
layout(location=1) in vec3 _normal;
layout(location=2) in vec3 _position;

layout(location=0) out vec4 fragColor;

uniform sampler2D colorSampler;

float rand(in float seed) {
    return fract(sin(seed) * 43758.5453123);
}

void main() {
    fragColor = vec4(vec3(rand(floor(_position.x + 0.001)), rand(floor(_position.y + 0.001)), rand(floor(_position.z + 0.001))) * max(dot(_normal, SUN_DIRECTION), AMBIENT), 1.0);
}