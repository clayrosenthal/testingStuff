/*
ZJ Wood CPE 471 Lab 3 base code
*/

#include <iostream>
#include <glad/glad.h>
#include <math.h>
#include <cstdlib>

#include "GLSL.h"
#include "Program.h"
#include "MatrixStack.h"

#include "WindowManager.h"
#include "Shape.h"

#include <glm/gtc/type_ptr.hpp>
#include <glm/gtc/matrix_transform.hpp>

#define CIRC_TRIS 100
#define NUM_INDICES (12*CIRC_TRIS)
#define SNOW_NUM 50

using namespace glm;
using namespace std;
double get_last_elapsed_time()
{
    static double lasttime = glfwGetTime();
    double actualtime =glfwGetTime();
    double difference = actualtime- lasttime;
    lasttime = actualtime;
    return difference;
}
class camera
{
public:
    glm::vec3 pos, rot;
    int w, a, s, d;
    camera()
    {
        w = a = s = d = 0;
        pos = glm::vec3(0, 0, -15);
        rot = glm::vec3(0, 0, 0);
    }
    glm::mat4 process(double frametime)
    {
        double ftime = frametime;
        float speed = 0;
        if (w == 1)
        {
            speed = 10*ftime;
        }
        else if (s == 1)
        {
            speed = -10*ftime;
        }
        float yangle=0;
        if (a == 1)
            yangle = -1*ftime;
        else if(d==1)
            yangle = 1*ftime;
        rot.y += yangle;
        glm::mat4 R = glm::rotate(glm::mat4(1), rot.y, glm::vec3(0, 1, 0));
        glm::vec4 dir = glm::vec4(0, 0, speed,1);
        dir = dir*R;
        pos += glm::vec3(dir.x, dir.y, dir.z);
        glm::mat4 T = glm::translate(glm::mat4(1), pos);
        return R*T;
    }
};

camera mycam;

class Application : public EventCallbacks
{

public:
    int kn = 0, ka = 0, kd = 0;
    WindowManager * windowManager = nullptr;

    // Our shader program
    std::shared_ptr<Program> prog, shapeprog;

    // Contains vertex information for OpenGL
    GLuint VertexArrayID, cylinderVAO, coneVAO;

    // Data necessary to give our box to OpenGL
    GLuint VertexBufferID, VertexColorIDBox, IndexBufferIDBox;
    GLuint cylinderVBO_coord, cylinderVBO_color, cylinderIBO, cylinderVBO_norm;
    GLuint coneVBO_coord, coneVBO_color, coneIBO, coneVBO_norm;

    Shape sphere;
    
    vec4 snowPoints[SNOW_NUM];

    void keyCallback(GLFWwindow *window, int key, int scancode, int action, int mods)
    {
        if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS)
        {
            glfwSetWindowShouldClose(window, GL_TRUE);
        }
        
        if (key == GLFW_KEY_W && action == GLFW_PRESS)
        {
            mycam.w = 1;
        }
        if (key == GLFW_KEY_W && action == GLFW_RELEASE)
        {
            mycam.w = 0;
        }
        if (key == GLFW_KEY_S && action == GLFW_PRESS)
        {
            mycam.s = 1;
        }
        if (key == GLFW_KEY_S && action == GLFW_RELEASE)
        {
            mycam.s = 0;
        }
        if (key == GLFW_KEY_A && action == GLFW_PRESS)
        {
//            mycam.a = 1;
            ka = 1;
        }
        if (key == GLFW_KEY_A && action == GLFW_RELEASE)
        {
//            mycam.a = 0;
            ka = 0;
        }
        if (key == GLFW_KEY_D && action == GLFW_PRESS)
        {
//            mycam.d = 1;
            kd = 1;
        }
        if (key == GLFW_KEY_D && action == GLFW_RELEASE)
        {
//            mycam.d = 0;
            kd = 0;
        }
        if (key == GLFW_KEY_N && action == GLFW_PRESS) kn = 1;
        if (key == GLFW_KEY_N && action == GLFW_RELEASE) kn = 0;
    }

    // callback for the mouse when clicked move the triangle when helper functions
    // written
    void mouseCallback(GLFWwindow *window, int button, int action, int mods)
    {
        double posX, posY;
        float newPt[2];
        if (action == GLFW_PRESS)
        {
            glfwGetCursorPos(window, &posX, &posY);
            std::cout << "Pos X " << posX <<  " Pos Y " << posY << std::endl;

        }
    }

    //if the window is resized, capture the new size and reset the viewport
    void resizeCallback(GLFWwindow *window, int in_width, int in_height)
    {
        //get the window size - may be different then pixels for retina
        int width, height;
        glfwGetFramebufferSize(window, &width, &height);
        glViewport(0, 0, width, height);
    }
    
    float randFloat(float min, float max)
    {
        return min + (rand() / ((float)RAND_MAX/(max - min)));
    }
    
    float randFloat1()
    {
        return rand() / ((float)RAND_MAX/1.0);
    }

    /*Note that any gl calls must always happen after a GL state is initialized */
    void initGeom()
    {
        string resourceDirectory = "../../resources";
        //try t800.obj or F18.obj ...
        sphere.loadMesh(resourceDirectory + "/sphere.obj");
        sphere.resize();
        sphere.init();

        // make snow points
        for(int s = 0; s < SNOW_NUM; s++)
        {
            snowPoints[s] = vec4(randFloat(-0.75, 0.75), randFloat(-0.75, 0.75), randFloat(-0.75, 0.75), randFloat1());
        }

        //generate the VAO
        glGenVertexArrays(1, &VertexArrayID);
        glBindVertexArray(VertexArrayID);

        //generate vertex buffer to hand off to OGL
        glGenBuffers(1, &VertexBufferID);
        //set the current state to focus on our vertex buffer
        glBindBuffer(GL_ARRAY_BUFFER, VertexBufferID);

        GLfloat cube_vertices[] = {
            // front
            -1.0, -1.0,  1.0,
            1.0, -1.0,  1.0,
            1.0,  1.0,  1.0,
            -1.0,  1.0,  1.0,
            // back
            -1.0, -1.0, -1.0,
            1.0, -1.0, -1.0,
            1.0,  1.0, -1.0,
            -1.0,  1.0, -1.0,
            //tube 8 - 11
            -1.0, -1.0,  1.0,
            1.0, -1.0,  1.0,
            1.0,  1.0,  1.0,
            -1.0,  1.0,  1.0,
            //12 - 15
            -1.0, -1.0, -1.0,
            1.0, -1.0, -1.0,
            1.0,  1.0, -1.0,
            -1.0,  1.0, -1.0

            
        };
        //actually memcopy the data - only do this once
        glBufferData(GL_ARRAY_BUFFER, sizeof(cube_vertices), cube_vertices, GL_DYNAMIC_DRAW);

        //we need to set up the vertex array
        glEnableVertexAttribArray(0);
        //key function to get up how many elements to pull out at a time (3)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, (void*) 0);

        //color
        GLfloat cube_colors[] = {
            // front colors
            1.0, 0.0, 0.5,
            1.0, 0.0, 0.5,
            1.0, 0.0, 0.5,
            1.0, 0.0, 0.5,
            // back colors
            0.5, 0.5, 0.0,
            0.5, 0.5, 0.0,
            0.5, 0.5, 0.0,
            0.5, 0.5, 0.0,
            // tube colors
            0.0, 1.0, 1.0,
            0.0, 1.0, 1.0,
            0.0, 1.0, 1.0,
            0.0, 1.0, 1.0,
            0.0, 1.0, 1.0,
            0.0, 1.0, 1.0,
            0.0, 1.0, 1.0,
            0.0, 1.0, 1.0,
        };
        glGenBuffers(1, &VertexColorIDBox);
        //set the current state to focus on our vertex buffer
        glBindBuffer(GL_ARRAY_BUFFER, VertexColorIDBox);
        glBufferData(GL_ARRAY_BUFFER, sizeof(cube_colors), cube_colors, GL_STATIC_DRAW);
        glEnableVertexAttribArray(1);
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, (void*)0);

        glGenBuffers(1, &IndexBufferIDBox);
        //set the current state to focus on our vertex buffer
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, IndexBufferIDBox);
        GLushort cube_elements[] = {
        
            // front
            0, 1, 2,
            2, 3, 0,
            // back
            7, 6, 5,
            5, 4, 7,
            //tube 8-11, 12-15
            8,12,13,
            8,13,9,
            9,13,14,
            9,14,10,
            10,14,15,
            10,15,11,
            11,15,12,
            11,12,8
            
        };
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(cube_elements), cube_elements, GL_STATIC_DRAW);
        // the cylinder
        //generate the VAO
        glGenVertexArrays(1, &cylinderVAO);
        glBindVertexArray(cylinderVAO);

        //generate vertex buffer to hand off to OGL
        glGenBuffers(1, &cylinderVBO_coord);
        //set the current state to focus on our vertex buffer
        glBindBuffer(GL_ARRAY_BUFFER, cylinderVBO_coord);
        
        glm::vec3 cylinderVertices[2*(1+CIRC_TRIS)];
        
        int i = 0;
        float a = 0, da = (2*M_PI/((float)CIRC_TRIS));
        cylinderVertices[0] = glm::vec3(0, 0, -0.5);
        cylinderVertices[CIRC_TRIS+1] = glm::vec3(0, 0, 0.5);
        
        for(i = 1; i <= CIRC_TRIS; i++)
        {
            cylinderVertices[i] = glm::vec3(0.5*cos(a), 0.5*sin(a), -0.5);
            cylinderVertices[i+1+CIRC_TRIS] = glm::vec3(0.5*cos(a), 0.5*sin(a), 0.5);
            a += da;
        }

        //actually memcopy the data - only do this once
        glBufferData(GL_ARRAY_BUFFER, sizeof(glm::vec3) * (2*(1+CIRC_TRIS)), cylinderVertices, GL_DYNAMIC_DRAW);

        //we need to set up the vertex array
        glEnableVertexAttribArray(0);
        //key function to get up how many elements to pull out at a time (3)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, (void*) 0);

        glGenBuffers(1, &cylinderVBO_color);
        //set the current state to focus on our vertex buffer
        glBindBuffer(GL_ARRAY_BUFFER, cylinderVBO_color);

        static glm::vec3 cylinderColorBuf[2*(1+CIRC_TRIS)];
        for (i = 0; i < 2*(1+CIRC_TRIS); i++)
        {
            cylinderColorBuf[i] = glm::vec3(0.9,0.9,0.9);
        }

        //actually memcopy the data - only do this once
        glBufferData(GL_ARRAY_BUFFER, sizeof(glm::vec3) * (2*(1+CIRC_TRIS)), cylinderColorBuf, GL_DYNAMIC_DRAW);

        //we need to set up the vertex array
        glEnableVertexAttribArray(1);
        //key function to get up how many elements to pull out at a time (3)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, (void*) 0);
        
        // normals
        glGenBuffers(1, &cylinderVBO_norm);
        //set the current state to focus on our vertex buffer
        glBindBuffer(GL_ARRAY_BUFFER, cylinderVBO_norm);

        static glm::vec3 cylinderNormalBuf[2*(1+CIRC_TRIS)];
        for (i = 0; i < 2*(1+CIRC_TRIS); i++)
        {
            if (cylinderVertices[i].x == 0 && cylinderVertices[i].y == 0)
            {
                cylinderNormalBuf[i] = glm::vec3(0, 0, cylinderVertices[i].z);
            }
            else
            {
                cylinderNormalBuf[i] = glm::vec3(cylinderVertices[i].x, cylinderVertices[i].y, 0);
            }
        }

        //actually memcopy the data - only do this once
        glBufferData(GL_ARRAY_BUFFER, sizeof(glm::vec3) * (2*(1+CIRC_TRIS)), cylinderNormalBuf, GL_DYNAMIC_DRAW);

        //we need to set up the vertex array
        glEnableVertexAttribArray(2);
        //key function to get up how many elements to pull out at a time (3)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, (void*) 0);

        glGenBuffers(1, &cylinderIBO);
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, cylinderIBO);

        static GLushort cylinderIndexBuffer[(int)NUM_INDICES];
        int triIndex = 1;
        for(i = 0; i < (NUM_INDICES/4)-3; i+=3)
        {
            // top and bottom
            cylinderIndexBuffer[i] = triIndex+1;
            cylinderIndexBuffer[i+(3*CIRC_TRIS)] = 1+CIRC_TRIS;
            cylinderIndexBuffer[i+1] = triIndex;
            cylinderIndexBuffer[i+(3*CIRC_TRIS)+1] = triIndex+CIRC_TRIS+1;
            cylinderIndexBuffer[i+2] = 0;
            cylinderIndexBuffer[i+(3*CIRC_TRIS)+2] = triIndex+CIRC_TRIS+2;
            
            // sides
            cylinderIndexBuffer[i+(6*CIRC_TRIS)] = triIndex;
            cylinderIndexBuffer[i+(6*CIRC_TRIS)+1] = triIndex+1;
            cylinderIndexBuffer[i+(6*CIRC_TRIS)+2] = triIndex+CIRC_TRIS+1;
            cylinderIndexBuffer[i+(9*CIRC_TRIS)] = triIndex+CIRC_TRIS+1;
            cylinderIndexBuffer[i+(9*CIRC_TRIS)+1] = triIndex+1;
            cylinderIndexBuffer[i+(9*CIRC_TRIS)+2] = triIndex+CIRC_TRIS+2;
            
            triIndex++;
        }
        //top and bottom
        cylinderIndexBuffer[i] = 1;
        cylinderIndexBuffer[i+(3*CIRC_TRIS)] = 1+CIRC_TRIS;
        cylinderIndexBuffer[i+1] = triIndex;
        cylinderIndexBuffer[i+(3*CIRC_TRIS)+1] = triIndex+CIRC_TRIS+1;
        cylinderIndexBuffer[i+2] = 0;
        cylinderIndexBuffer[i+(3*CIRC_TRIS)+2] = CIRC_TRIS+2;
        
        //sides
        cylinderIndexBuffer[i+(6*CIRC_TRIS)] = triIndex;
        cylinderIndexBuffer[i+(6*CIRC_TRIS)+1] = 1;
        cylinderIndexBuffer[i+(6*CIRC_TRIS)+2] = triIndex+CIRC_TRIS+1;
        cylinderIndexBuffer[i+(9*CIRC_TRIS)] = triIndex+CIRC_TRIS+1;
        cylinderIndexBuffer[i+(9*CIRC_TRIS)+1] = 1;
        cylinderIndexBuffer[i+(9*CIRC_TRIS)+2] = CIRC_TRIS+2;

        glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(GLushort) * (NUM_INDICES), cylinderIndexBuffer, GL_DYNAMIC_DRAW);
        
        // the cone
        //generate the VAO
        glGenVertexArrays(1, &coneVAO);
        glBindVertexArray(coneVAO);

        //generate vertex buffer to hand off to OGL
        glGenBuffers(1, &coneVBO_coord);
        //set the current state to focus on our vertex buffer
        glBindBuffer(GL_ARRAY_BUFFER, coneVBO_coord);
        
        glm::vec3 coneVertices[(2+CIRC_TRIS)];
        
        i = 0;
        a = 0;
        coneVertices[0] = glm::vec3(0, 0, -0.5);
        coneVertices[CIRC_TRIS+1] = glm::vec3(0, 0, 0.5);
        
        for(i = 1; i <= CIRC_TRIS; i++)
        {
            coneVertices[i] = glm::vec3(0.5*cos(a), 0.5*sin(a), -0.5);
            a += da;
        }

        //actually memcopy the data - only do this once
        glBufferData(GL_ARRAY_BUFFER, sizeof(glm::vec3) * (2+CIRC_TRIS), coneVertices, GL_DYNAMIC_DRAW);

        //we need to set up the vertex array
        glEnableVertexAttribArray(0);
        //key function to get up how many elements to pull out at a time (3)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, (void*) 0);

        glGenBuffers(1, &coneVBO_color);
        //set the current state to focus on our vertex buffer
        glBindBuffer(GL_ARRAY_BUFFER, coneVBO_color);

        static glm::vec3 coneColorBuf[(2+CIRC_TRIS)];
        for (i = 0; i < (2+CIRC_TRIS); i++)
        {
            coneColorBuf[i] = glm::vec3(0.9,0.9,0.9);
        }

        //actually memcopy the data - only do this once
        glBufferData(GL_ARRAY_BUFFER, sizeof(glm::vec3) * (2+CIRC_TRIS), coneColorBuf, GL_DYNAMIC_DRAW);

        //we need to set up the vertex array
        glEnableVertexAttribArray(1);
        //key function to get up how many elements to pull out at a time (3)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, (void*) 0);
        
        // normals
        glGenBuffers(1, &coneVBO_norm);
        //set the current state to focus on our vertex buffer
        glBindBuffer(GL_ARRAY_BUFFER, coneVBO_norm);

        static glm::vec3 coneNormalBuf[(2+CIRC_TRIS)];
        for (i = 0; i < (2+CIRC_TRIS); i++)
        {
            if (coneVertices[i].x == 0 && coneVertices[i].y == 0)
            {
                coneNormalBuf[i] = glm::vec3(0, 0, coneVertices[i].z);
            }
            else
            {
                coneNormalBuf[i] = glm::vec3(coneVertices[i].x, coneVertices[i].y, 0);
            }
        }

        //actually memcopy the data - only do this once
        glBufferData(GL_ARRAY_BUFFER, sizeof(glm::vec3) * (2+CIRC_TRIS), coneNormalBuf, GL_DYNAMIC_DRAW);

        //we need to set up the vertex array
        glEnableVertexAttribArray(2);
        //key function to get up how many elements to pull out at a time (3)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, (void*) 0);

        glGenBuffers(1, &coneIBO);
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, coneIBO);

        static GLushort coneIndexBuffer[(int)(NUM_INDICES/2)];
        triIndex = 1;
        for(i = 0; i < (NUM_INDICES/4)-3; i+=3)
        {
            // bottom and sides
            coneIndexBuffer[i] = triIndex+1;
            coneIndexBuffer[i+(3*CIRC_TRIS)] = 1+CIRC_TRIS;
            coneIndexBuffer[i+1] = triIndex;
            coneIndexBuffer[i+(3*CIRC_TRIS)+1] = triIndex;
            coneIndexBuffer[i+2] = 0;
            coneIndexBuffer[i+(3*CIRC_TRIS)+2] = triIndex+1;
            
            
            triIndex++;
        }
        //top and bottom
        coneIndexBuffer[i] = 0;
        coneIndexBuffer[i+(3*CIRC_TRIS)] = 1+CIRC_TRIS;
        coneIndexBuffer[i+1] = triIndex;
        coneIndexBuffer[i+(3*CIRC_TRIS)+1] = triIndex;
        coneIndexBuffer[i+2] = 1;
        coneIndexBuffer[i+(3*CIRC_TRIS)+2] = 1;

        glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(GLushort) * (NUM_INDICES/2), coneIndexBuffer, GL_DYNAMIC_DRAW);


        glBindVertexArray(0);

    }

    //General OGL initialization - set OGL state here
    void init(const std::string& resourceDirectory)
    {
        GLSL::checkVersion();

        // Set background color.
        glClearColor(0.1f, 0.1f, 0.1f, 1.0f);
        // Enable z-buffer test.
        glEnable(GL_DEPTH_TEST);
        // Enable blending/transparency
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        // Enable culling
        glEnable(GL_CULL_FACE);
        glFrontFace(GL_CCW);
        

        // Initialize the GLSL program.
        prog = std::make_shared<Program>();
        prog->setVerbose(true);
        prog->setShaderNames(resourceDirectory + "/shader_vertex.glsl", resourceDirectory + "/shader_fragment.glsl");
        if (!prog->init())
            {
            std::cerr << "One or more shaders failed to compile... exiting!" << std::endl;
            exit(1); //make a breakpoint here and check the output window for the error message!
            }
        prog->addUniform("P");
        prog->addUniform("V");
        prog->addUniform("M");
        prog->addUniform("shapeCol");
        prog->addAttribute("vertPos");
        prog->addAttribute("vertColor");
        prog->addAttribute("vertNor");
        // Initialize the GLSL program.
        shapeprog = std::make_shared<Program>();
        shapeprog->setVerbose(true);
        shapeprog->setShaderNames(resourceDirectory + "/shape_vertex.glsl", resourceDirectory + "/shape_fragment.glsl");
        if (!shapeprog->init())
            {
            std::cerr << "One or more shaders failed to compile... exiting!" << std::endl;
            exit(1); //make a breakpoint here and check the output window for the error message!
            }
        shapeprog->addUniform("P");
        shapeprog->addUniform("V");
        shapeprog->addUniform("M");
        shapeprog->addUniform("alpha");
        shapeprog->addUniform("shapeCol");
        shapeprog->addAttribute("vertPos");
        shapeprog->addAttribute("vertNor");
        shapeprog->addAttribute("vertTex");
    }
    
    void makeBoosters(mat4 M, mat4 M_parent, mat4 S)
    {
        // has to be called while coneVAO is bound
        mat4 S_nozzle, T_N_noz, R_N_noz, M_N_noz;
        S_nozzle = glm::scale(glm::mat4(1.0f), glm::vec3(0.35, 0.35, 0.32));
        T_N_noz = glm::translate(glm::mat4(1.0f), glm::vec3(0, 0.2, 0.5));
        R_N_noz = glm::rotate(glm::mat4(1.0f), (float)M_PI, glm::vec3(1.0f, 0.0f, 0.0f));
        M_N_noz = M_parent * S * T_N_noz * R_N_noz;
        
        M = M_N_noz * S_nozzle;
        
        glUniformMatrix4fv(prog->getUniform("M"), 1, GL_FALSE, &M[0][0]);
        glUniform3f(prog->getUniform("shapeCol"), 0.6, 0.6, 0.6);
        glDrawElements(GL_TRIANGLES, NUM_INDICES/2, GL_UNSIGNED_SHORT, (void*)0);
        
        mat4 T_S_noz, R_S_noz, M_S_noz;
        T_S_noz = glm::translate(glm::mat4(1.0f), glm::vec3(0, -0.2, 0.5));
        R_S_noz = glm::rotate(glm::mat4(1.0f), (float)M_PI, glm::vec3(1.0f, 0.0f, 0.0f));
        M_S_noz = M_parent * S * T_S_noz * R_S_noz;
        
        M = M_S_noz * S_nozzle;
        
        glUniformMatrix4fv(prog->getUniform("M"), 1, GL_FALSE, &M[0][0]);
        glDrawElements(GL_TRIANGLES, NUM_INDICES/2, GL_UNSIGNED_SHORT, (void*)0);
        
        mat4 T_W_noz, R_W_noz, M_W_noz;
        T_W_noz = glm::translate(glm::mat4(1.0f), glm::vec3(0.2, 0, 0.5));
        R_W_noz = glm::rotate(glm::mat4(1.0f), (float)M_PI, glm::vec3(1.0f, 0.0f, 0.0f));
        M_W_noz = M_parent * S * T_W_noz * R_W_noz;
        
        M = M_W_noz * S_nozzle;
        
        glUniformMatrix4fv(prog->getUniform("M"), 1, GL_FALSE, &M[0][0]);
        glDrawElements(GL_TRIANGLES, NUM_INDICES/2, GL_UNSIGNED_SHORT, (void*)0);
        
        mat4 T_E_noz, R_E_noz, M_E_noz;
        T_E_noz = glm::translate(glm::mat4(1.0f), glm::vec3(-0.2, 0, 0.5));
        R_E_noz = glm::rotate(glm::mat4(1.0f), (float)M_PI, glm::vec3(1.0f, 0.0f, 0.0f));
        M_E_noz = M_parent * S * T_E_noz * R_E_noz;
        
        M = M_E_noz * S_nozzle;
        
        glUniformMatrix4fv(prog->getUniform("M"), 1, GL_FALSE, &M[0][0]);
        glDrawElements(GL_TRIANGLES, NUM_INDICES/2, GL_UNSIGNED_SHORT, (void*)0);
        
        mat4 S_booster;
        S_booster = glm::scale(glm::mat4(1.0f), glm::vec3(0.3, 0.3, 0.4));
        
        
        mat4 T_N_boos, R_N_boos, M_N_boos;
        T_N_boos = glm::translate(glm::mat4(1.0f), glm::vec3(0, 0, -0.2));
        M_N_boos = M_N_noz * T_N_boos * R_N_boos;
        
        M = M_N_boos * S_booster;
        glUniformMatrix4fv(prog->getUniform("M"), 1, GL_FALSE, &M[0][0]);
        glUniform3f(prog->getUniform("shapeCol"), 1, 0.6, 0.6);
        glDrawElements(GL_TRIANGLES, NUM_INDICES/2, GL_UNSIGNED_SHORT, (void*)0);
        
        mat4 T_S_boos, R_S_boos, M_S_boos;
        T_S_boos = glm::translate(glm::mat4(1.0f), glm::vec3(0, 0, -0.2));
        M_S_boos = M_S_noz * T_S_boos * R_S_boos;
        
        M = M_S_boos * S_booster;
        glUniformMatrix4fv(prog->getUniform("M"), 1, GL_FALSE, &M[0][0]);
        glDrawElements(GL_TRIANGLES, NUM_INDICES/2, GL_UNSIGNED_SHORT, (void*)0);
        
        mat4 T_E_boos, R_E_boos, M_E_boos;
        T_E_boos = glm::translate(glm::mat4(1.0f), glm::vec3(0, 0, -0.2));
        M_E_boos = M_E_noz * T_E_boos * R_E_boos;
        
        M = M_E_boos * S_booster;
        glUniformMatrix4fv(prog->getUniform("M"), 1, GL_FALSE, &M[0][0]);
        glDrawElements(GL_TRIANGLES, NUM_INDICES/2, GL_UNSIGNED_SHORT, (void*)0);
        
        mat4 T_W_boos, R_W_boos, M_W_boos;
        T_W_boos = glm::translate(glm::mat4(1.0f), glm::vec3(0, 0, -0.2));
        M_W_boos = M_W_noz * T_W_boos * R_W_boos;
        
        M = M_W_boos * S_booster;
        glUniformMatrix4fv(prog->getUniform("M"), 1, GL_FALSE, &M[0][0]);
        glDrawElements(GL_TRIANGLES, NUM_INDICES/2, GL_UNSIGNED_SHORT, (void*)0);
    }
    
    void makeSnow(mat4 M, vec4 start, float time, mat4 R)
    {
        mat4 S_snow = glm::scale(glm::mat4(1.0f), glm::vec3(0.02, 0.02, 0.02));
        mat4 T_snow = glm::translate(glm::mat4(1.0f), glm::vec3(start[0] + start[3] *cos(time), start[1] + start[3] * cos(time) * sin(time), start[2] + start[3] * sin(time)));
        M = T_snow * R * S_snow;
        glUniformMatrix4fv(shapeprog->getUniform("M"), 1, GL_FALSE, &M[0][0]);
        sphere.draw(shapeprog);
    }


    /****DRAW
    This is the most important function in your program - this is where you
    will actually issue the commands to draw any geometry you have set up to
    draw
    ********/
    void render()
    {

        double frametime = get_last_elapsed_time();
        // Get current frame buffer size.
        int width, height;
        glfwGetFramebufferSize(windowManager->getHandle(), &width, &height);
        float aspect = width/(float)height;
        glViewport(0, 0, width, height);
        //glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
        // Clear framebuffer.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        // Create the matrix stacks - please leave these alone for now
        
        glm::mat4 V, M, P; //View, Model and Perspective matrix
        V = glm::mat4(1);
        M = glm::mat4(1);
        // Apply orthographic projection....
        P = glm::perspective((float)(3.14159 / 4.), (float)((float)width/ (float)height), 0.1f, 1000.0f); //so much type casting... GLM metods are quite funny ones

        
        // Draw the box using GLSL.
        prog->bind();

        glFrontFace(GL_CCW);
        V = mycam.process(frametime);
        
        mat4 S_lowerCyl, T_lowerCyl, R_lowerCyl, M_lowerCyl;
        mat4 R_cylX, R_cylY, R_cylZ;
        
        static float move = 0;
        move += 0.01;
        float sinMove = sin(move) * 0.5 + 0.5;
        const float cosMove = 1 - sinMove;
        
        static float w = 0;
        w += 0.02 * ka;
        w -= 0.02 * kd;
       
        R_cylX = glm::rotate(glm::mat4(1.0f), 1.57f, glm::vec3(1.0f, 0.0f, 0.0f));
        R_cylY = glm::rotate(glm::mat4(1.0f), -0.3f, glm::vec3(0.0f, 1.0f, 0.0f));
        R_cylZ = glm::rotate(glm::mat4(1.0f), w, glm::vec3(0.0f, 0.0f, 1.0f));
        S_lowerCyl = glm::scale(glm::mat4(1.0f), glm::vec3(0.6, 0.6, 1.3));
        T_lowerCyl = glm::translate(glm::mat4(1.0f), glm::vec3(0, -0.25, -1));
        M_lowerCyl = T_lowerCyl * R_cylX * R_cylZ * R_cylY;// * R_lowerCyl;
        
        M = M_lowerCyl * S_lowerCyl;
        
        
        glBindVertexArray(cylinderVAO);
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, cylinderIBO);
        glUniformMatrix4fv(prog->getUniform("P"), 1, GL_FALSE, &P[0][0]);
        glUniformMatrix4fv(prog->getUniform("V"), 1, GL_FALSE, &V[0][0]);
        glUniformMatrix4fv(prog->getUniform("M"), 1, GL_FALSE, &M[0][0]);
        glUniform3f(prog->getUniform("shapeCol"), 0.8, 0.8, 0.8);
        glDrawElements(GL_TRIANGLES, NUM_INDICES, GL_UNSIGNED_SHORT, (void*)0);
        
        
        mat4 S_cyl, T_cyl, M_cyl;
        S_cyl = glm::scale(glm::mat4(1.0f), glm::vec3(0.5, 0.5, 0.9));
        T_cyl = glm::translate(glm::mat4(1.0f), glm::vec3(0, 0, -1 - 0.3*sinMove));
        
        M_cyl = M_lowerCyl * T_cyl;
        
        M = M_cyl * S_cyl;
        
        glUniformMatrix4fv(prog->getUniform("M"), 1, GL_FALSE, &M[0][0]);
        glUniform3f(prog->getUniform("shapeCol"), 0.6, 0.6, 0.6);
        glDrawElements(GL_TRIANGLES, NUM_INDICES, GL_UNSIGNED_SHORT, (void*)0);
        
        // side boosters
        
        mat4 S_anim = glm::scale(glm::mat4(1.0f), glm::vec3(cosMove, cosMove, cosMove));
        mat4 S_side_rocket = glm::scale(glm::mat4(1.0f), glm::vec3(0.6, 0.6, 1.3));
        
        mat4 M_L_rocket, T_L_rocket, R_side_rocket, R_anim, T_anim;
        R_side_rocket = glm::rotate(glm::mat4(1.0f), (float)M_PI/4.0f, glm::vec3(0.0f, 0.0f, 1.0f));
        T_L_rocket = glm::translate(glm::mat4(1.0f), glm::vec3(0.6, 0, 2));
        R_anim = glm::rotate(glm::mat4(1.0f), -sinMove*0.5f, glm::vec3(0.0f, 1.0f, 0.0f));
        T_anim = glm::translate(glm::mat4(1.0f), glm::vec3(0, 0, -2));
        M_L_rocket = M_lowerCyl * T_L_rocket * R_side_rocket * R_anim * T_anim;
        M = M_L_rocket * S_side_rocket * S_anim;
        glUniformMatrix4fv(prog->getUniform("M"), 1, GL_FALSE, &M[0][0]);
        glUniform3f(prog->getUniform("shapeCol"), 0.8, 0.8, 0.8);
        glDrawElements(GL_TRIANGLES, NUM_INDICES, GL_UNSIGNED_SHORT, (void*)0);
        
        mat4 M_R_rocket, T_R_rocket;
        T_R_rocket = glm::translate(glm::mat4(1.0f), glm::vec3(-0.6, 0, 2));
        R_anim = glm::rotate(glm::mat4(1.0f), sinMove*0.5f, glm::vec3(0.0f, 1.0f, 0.0f));
        M_R_rocket = M_lowerCyl * T_R_rocket * R_side_rocket * R_anim * T_anim;
        
        M = M_R_rocket * S_side_rocket * S_anim;
        glUniformMatrix4fv(prog->getUniform("M"), 1, GL_FALSE, &M[0][0]);
        glDrawElements(GL_TRIANGLES, NUM_INDICES, GL_UNSIGNED_SHORT, (void*)0);
        
        glBindVertexArray(0);
        
        
        mat4 S_nose, T_nose, R_nose, M_nose;
        S_nose = glm::scale(glm::mat4(1.0f), glm::vec3(0.5, 0.5, 0.5));
        T_nose = glm::translate(glm::mat4(1.0f), glm::vec3(0, 0, -0.7));
        R_nose = glm::rotate(glm::mat4(1.0f), (float)M_PI, glm::vec3(1.0f, 0.0f, 0.0f));
        M_nose = M_cyl * T_nose * R_nose;
        
        M = M_nose * S_nose;
        glBindVertexArray(coneVAO);
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, coneIBO);
        glUniformMatrix4fv(prog->getUniform("P"), 1, GL_FALSE, &P[0][0]);
        glUniformMatrix4fv(prog->getUniform("V"), 1, GL_FALSE, &V[0][0]);
        glUniformMatrix4fv(prog->getUniform("M"), 1, GL_FALSE, &M[0][0]);
        glUniform3f(prog->getUniform("shapeCol"), 0.6, 0.6, 0.6);
        glDrawElements(GL_TRIANGLES, NUM_INDICES/2, GL_UNSIGNED_SHORT, (void*)0);
        
        
        makeBoosters(M, M_lowerCyl, mat4(1.0f));
        
        // left side
        makeBoosters(M, M_L_rocket, S_anim);
        
        // right side
        makeBoosters(M, M_R_rocket, S_anim);
        
        
        glBindVertexArray(0);
        prog->unbind();


        shapeprog->bind();
        glUniformMatrix4fv(shapeprog->getUniform("P"), 1, GL_FALSE, &P[0][0]);
        glUniformMatrix4fv(shapeprog->getUniform("V"), 1, GL_FALSE, &V[0][0]);
        
        mat4 S_caps;
        S_caps = glm::scale(glm::mat4(1.0f), glm::vec3(0.3, 0.3, 0.5));
        
        mat4 T_L_cap, M_L_cap;
        
        T_L_cap = glm::translate(glm::mat4(1.0f), glm::vec3(0, 0, -0.65));
        M_L_cap = M_L_rocket * S_anim * T_L_cap;
        M = M_L_cap * S_caps;
        glUniformMatrix4fv(shapeprog->getUniform("M"), 1, GL_FALSE, &M[0][0]);
        glUniform3f(shapeprog->getUniform("shapeCol"), 0.9, 0.9, 0.9);
        glUniform1f(shapeprog->getUniform("alpha"), 1);
        sphere.draw(shapeprog);
        
        mat4 T_R_cap, M_R_cap;
        
        T_R_cap = glm::translate(glm::mat4(1.0f), glm::vec3(0, 0, -0.65));
        M_R_cap = M_R_rocket * S_anim * T_L_cap;
        M = M_R_cap * S_caps;
        glUniformMatrix4fv(shapeprog->getUniform("M"), 1, GL_FALSE, &M[0][0]);
        sphere.draw(shapeprog);
        
        
        glUniform3f(shapeprog->getUniform("shapeCol"), 1, 1, 1);
        glUniform1f(shapeprog->getUniform("alpha"), 0.5);
        mat4 R_globe = glm::rotate(glm::mat4(1.0f), (float)(M_PI/2.0f), glm::vec3(1, 0, 0));
        static float sn_time = 0;
        sn_time += 0.01;
        
        for (int snow = 0; snow < SNOW_NUM; snow++)
        {
            if (snow % 2 == 0)
                makeSnow(M, snowPoints[snow], sn_time, R_globe * R_cylZ);
            else
                makeSnow(M, snowPoints[snow], -1*sn_time, R_globe * R_cylZ);
        }
        
        mat4 S_globe = glm::scale(glm::mat4(1.0f), glm::vec3(2, 2, 2));
        mat4 T_globe = glm::translate(glm::mat4(1.0f), glm::vec3(0, 0, 0));
        mat4 M_globe = T_globe * R_globe * R_cylZ;
        M = M_globe * S_globe;
        glUniformMatrix4fv(shapeprog->getUniform("M"), 1, GL_FALSE, &M[0][0]);
        glUniform3f(shapeprog->getUniform("shapeCol"), 0.8, 0.8, 1);
        glUniform1f(shapeprog->getUniform("alpha"), 0.5);
        sphere.draw(shapeprog);
        
        glFrontFace(GL_CW);
        sphere.draw(shapeprog);
//        
//        mat4 T_mini = glm::translate(glm::mat4(1.0f), glm::vec3(1, 0, 0));
//        S_sphere = glm::scale(glm::mat4(1.0f), glm::vec3(0.5, 0.5, 0.5));
//        M = M_sphere * T_mini * S_sphere;
//        glUniformMatrix4fv(shapeprog->getUniform("M"), 1, GL_FALSE, &M[0][0]);
//        sphere.draw(shapeprog);
        
        shapeprog->unbind();

    }

};
//******************************************************************************************
int main(int argc, char **argv)
{
    std::string resourceDir = "../../resources"; // Where the resources are loaded from
    if (argc >= 2)
    {
        resourceDir = argv[1];
    }

    Application *application = new Application();

    /* your main will always include a similar set up to establish your window
        and GL context, etc. */
    WindowManager * windowManager = new WindowManager();
    windowManager->init(1920, 1080);
    windowManager->setEventCallbacks(application);
    application->windowManager = windowManager;

    /* This is the code that will likely change program to program as you
        may need to initialize or set up different data and state */
    // Initialize scene.
    application->init(resourceDir);
    application->initGeom();

    // Loop until the user closes the window.
    while(! glfwWindowShouldClose(windowManager->getHandle()))
    {
        // Render scene.
        application->render();

        // Swap front and back buffers.
        glfwSwapBuffers(windowManager->getHandle());
        // Poll for and process events.
        glfwPollEvents();
    }

    // Quit program.
    windowManager->shutdown();
    return 0;
}
