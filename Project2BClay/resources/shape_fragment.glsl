#version 330 core
out vec4 color;

in vec3 fragTex;
in vec3 fragNor;
in vec3 fragPos;

uniform vec3 shapeCol;
uniform float alpha;

void main()
{
    vec3 lightPos = vec3(15,30,-1);
    vec3 lightDir = normalize((lightPos - fragPos));
    vec3 normal = normalize(fragNor);
    float diffFact = 0.4 + 0.6 * dot(lightDir, normal);
    color.rgb = shapeCol*diffFact;
    color.a=alpha;	//transparency: 1 .. 100% NOT transparent
}
