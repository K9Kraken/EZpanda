#version 330


uniform mat4 p3d_ModelViewProjectionMatrix;
uniform samplerBuffer texbuffer;

in vec3 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;

out vec2 texcoord;

void main() {
    texcoord = p3d_MultiTexCoord0;
    vec4 instance = texelFetch(texbuffer, gl_InstanceID);
    gl_Position = p3d_ModelViewProjectionMatrix * vec4(p3d_Vertex*instance.w + instance.xyz, 1);
}



#version 330


uniform sampler2D texture0;

in vec2 texcoord;

out vec4 color;

void main() {
    vec4 diffuse = texture(texture0, texcoord);
    color = diffuse;
}
