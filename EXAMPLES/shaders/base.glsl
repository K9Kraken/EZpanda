#version 330

uniform mat4 p3d_ModelViewProjectionMatrix;
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;

out vec2 texcoord;

void main(void){
    texcoord = p3d_MultiTexCoord0;
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
}



#version 330

uniform sampler2D texture0;

in vec2 texcoord;

out vec4 color;

void main (void){
    vec4 diffuse = texture(texture0, texcoord);
    color = diffuse;
}