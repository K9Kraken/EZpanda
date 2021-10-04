#version 330


uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelViewMatrix;
in vec4 p3d_Vertex;

//uniform sampler2D depth;
out vec4 verts;
out vec4 model_verts;

void main(void){
    model_verts = p3d_ModelViewMatrix * p3d_Vertex;
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    verts = p3d_Vertex;
}


#version 330


uniform sampler2D depth_map;
uniform vec2 depth_resolution;
uniform float near;
uniform float far;

in vec4 verts;
in vec4 model_verts;

out vec4 color;



float linearize( float sample){
  return (2.0 * near) / (far + near - (2.0 * sample - 1.0) * (far - near));
}


void main (void){
    float depth_sample = texture(depth_map, gl_FragCoord.xy / depth_resolution).r;
    float water_depth = linearize(depth_sample) - linearize(gl_FragCoord.z);

    float alpha = smoothstep(0.0, 1.0, water_depth*200);

    color = vec4(0.2, 0.3, 0.8, alpha);
}
