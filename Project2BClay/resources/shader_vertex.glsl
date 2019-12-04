#version 330 core
layout(location = 0) in vec3 vertPos;
layout(location = 1) in vec3 vertColor;
layout(location = 2) in vec3 vertNor;
uniform mat4 P;
uniform mat4 V;
uniform mat4 M;

out vec3 vertex_pos;
out vec3 vertex_color;
out vec3 vertex_norm;

void main()
{
    vertex_pos = vertPos;
    vertex_norm = vec4(M * vec4(vertNor, 0.0)).xyz;
	vertex_color = vertColor;
	gl_Position = P * V * M * vec4(vertPos, 1.0);
}
