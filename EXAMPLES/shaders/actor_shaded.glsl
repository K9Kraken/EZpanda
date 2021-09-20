#version 330

uniform mat4 p3d_ViewProjectionMatrix;
uniform mat4 p3d_ModelMatrix;

uniform mat4 p3d_TransformTable[100];
in vec4 transform_weight;
in uvec4 transform_index;

in vec4 vertex;
in vec3 normal;
in vec2 p3d_MultiTexCoord0;

out vec2 texcoord;
out vec3 world_normal;

out vec3 pos;

void main(void){
    mat4 anim_matrix = p3d_ModelMatrix * (p3d_TransformTable[transform_index.x] * transform_weight.x
          + p3d_TransformTable[transform_index.y] * transform_weight.y
          + p3d_TransformTable[transform_index.z] * transform_weight.z
          + p3d_TransformTable[transform_index.w] * transform_weight.w);


    world_normal = (anim_matrix * vec4(normal, 0.0)).xyz;

    texcoord = p3d_MultiTexCoord0;
    gl_Position = p3d_ViewProjectionMatrix * anim_matrix * vertex;
}



#version 330

uniform sampler2D texture0;

in vec2 texcoord;
in vec3 world_normal;
in vec3 pos;


out vec4 color;

float ambience = 0.2;

vec3 dir = normalize(vec3(10.0, 0.0, 10.0));

void main (void){
    vec4 diffuse = texture(texture0, texcoord);

    float light = max(dot(world_normal, dir)*2.0, ambience);

    color = vec4(diffuse.rgb*light, diffuse.a);
}
