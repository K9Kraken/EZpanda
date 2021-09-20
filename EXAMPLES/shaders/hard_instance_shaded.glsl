#version 330


uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelMatrix;
uniform samplerBuffer texbuffer;

in vec3 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;

in vec3 normal;

out vec2 texcoord;
out vec3 world_normal;

void main() {
    texcoord = p3d_MultiTexCoord0;
    vec4 instance = texelFetch(texbuffer, gl_InstanceID);

    world_normal = (p3d_ModelMatrix * vec4(normal, 0.0)).xyz;
    gl_Position = p3d_ModelViewProjectionMatrix * vec4(p3d_Vertex*instance.w + instance.xyz, 1);
}



#version 330



uniform sampler2D texture0;

in vec2 texcoord;
in vec3 world_normal;

out vec4 color;

float ambience = 0.3;
vec3 direction = vec3(3.0, -2.0, 5.0);

void main() {
    vec4 diffuse = texture(texture0, texcoord);
    float light = dot(world_normal, normalize(direction))+0.5;
    color = vec4(diffuse.rgb*light, diffuse.a);
}
