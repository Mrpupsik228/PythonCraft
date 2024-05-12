#version 410
#define SUN_DIRECTION normalize(vec3(0.7, 0.8, 0.3))
#define AMBIENT 0.5

layout(location=0) in vec2 _texcoord;
layout(location=1) in vec3 _normal;

layout(location=0) out vec4 fragColor;

uniform sampler2D colorSampler;

void main() {
    fragColor = texture2D(colorSampler, _texcoord);
    fragColor.rgb *= max(dot(SUN_DIRECTION, _normal), AMBIENT);
}