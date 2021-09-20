#version 330



struct p3d_LightSourceParameters {
    vec4 color;
    vec3 spotDirection;
    sampler2DShadow shadowMap;
    mat4 shadowViewMatrix;
};
uniform p3d_LightSourceParameters sun;

uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelViewMatrix;

in vec4 p3d_Vertex;

out vec4 shadow_uv;


void main(void){
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    shadow_uv = sun.shadowViewMatrix * (p3d_ModelViewMatrix * p3d_Vertex);

}


#version 330



 struct p3d_LightSourceParameters {
    vec4 color;
    vec3 spotDirection;
    sampler2DShadow shadowMap;
    mat4 shadowViewMatrix;
};
uniform p3d_LightSourceParameters sun;


in vec4 shadow_uv;

out vec4 color;


void main (void){
    float shadow = textureProj(sun.shadowMap, shadow_uv);
    color = vec4(0.8, 0.8, 0.8, 1.0)*shadow; //*(shadow+0.5);
}