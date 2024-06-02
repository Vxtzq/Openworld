#version 130

uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelMatrix;
uniform float time;

in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;

out vec2 texcoord;
out vec3 worldPosition;

void main() {
    vec4 worldPos = p3d_ModelMatrix * p3d_Vertex;
    worldPosition = worldPos.xyz;
    texcoord = p3d_MultiTexCoord0 + vec2(sin(time + p3d_Vertex.x * 0.1) * 0.01, cos(time + p3d_Vertex.z * 0.1) * 0.01);
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
}