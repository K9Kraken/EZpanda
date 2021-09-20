#version 330



uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelMatrix;
uniform mat4 p3d_ViewMatrix;

in vec2 p3d_MultiTexCoord0;

in vec4 vertex;
in vec3 normal;


out vec2 texcoord;
out vec3 world_normal;

void main(void){
    texcoord = p3d_MultiTexCoord0;

    world_normal = (p3d_ModelMatrix * vec4(normal, 0.0)).xyz;
    gl_Position = p3d_ModelViewProjectionMatrix * vertex;
}



#version 330



uniform sampler2D texture0;

in vec2 texcoord;
in vec3 world_normal;

out vec4 color;

float ambience = 0.4;
vec3 direction = vec3(0.0, 2.0, 4.0);

void main (void){
    vec4 diffuse = texture(texture0, texcoord);
    float light = max(dot(world_normal, normalize(direction))+0.5, ambience);

    color = vec4(diffuse.rgb*light, diffuse.a);
}