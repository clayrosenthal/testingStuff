#version 330 core
out vec4 color;

in vec3 vertex_pos;
in vec3 vertex_color;
in vec3 vertex_norm;

uniform vec3 shapeCol;

void main()
{
    vec3 lightPos = vec3(15,30,-1);
    vec3 lightDir = normalize((lightPos - vertex_pos));
    vec3 fragNorm = normalize(vertex_norm);
    float diffFact = 0.4 + 0.6 * dot(lightDir, fragNorm);
    color.rgb = shapeCol * diffFact;
	color.a=1;	//transparency: 1 .. 100% NOT transparent
}
