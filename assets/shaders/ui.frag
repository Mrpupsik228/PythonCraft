#version 410

layout(location=0) in vec2 _texcoord;
layout(location=0) out vec4 fragColor;

uniform bool hasTexture;
uniform sampler2D colorSampler;

void main() {
    fragColor = hasTexture ? texture2D(colorSampler, _texcoord) : vec4(1.0);
}