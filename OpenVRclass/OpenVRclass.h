//##############################################################################################################################################################
//
//
//						OpenVR class for OpenGL application
//
///			By Christian Eckhardt, ceckhard@calpoly.edu
//
//
///			Code uses the program class for "easier" shader implementation, which comes with this package
///			Program class by Ian Dunn and Zoe" Wood (Cal Poly).
//
//
///			incudes:		OpenVRclass.cpp
///							OpenVRclass.h
///							Program.cpp
///							Program.h
///							FBOvertex.glsl
///							FBOfragment.glsl
//
//--------------------------------------------------------------------------------------------------------------------------------------------------------------
//
//			USAGE
//
//			1. Make a global pointer of the VR class in your application (main file):
///				OpenVRApplication *vrapp = NULL;
//
//			2. After having created the window, make an instance:
///				vrapp = new OpenVRApplication;
//
//			2.5 Initialize your screen-window with the size given from the VR class
///				i.e.: windowManager->init(vrapp->get_render_width(), vrapp->get_render_height());
//
//
//			3. After initialize OpenGL, initialize the buffers for the VR class:
///				vrapp->init_buffers(resourceDirectory);//resourceDirectory .. where the GLSL shader files can be found
//
//			4. write your render function:
///				your_render_fct(int width, int height, glm::mat4 VRheadmatrix);	//the paramteres will be provided by the class itself later
///				{
///				DO NOT SET following stuff in here (because it will be set by the class):
///					- framebuffer
///					- viewport
///				assign your view matrix (or multiply it) with VRheadmatrix
///				assign your P matrix with:
///					vr::Hmd_Eye currenteye;
///					if (eye == LEFTEYE)		currenteye = vr::Eye_Left;	else		currenteye = vr::Eye_Right;
///					if (!vrapp->get_projection_matrix(currenteye, 0.1f, 1000.0f, P))
///					P = glm::perspective((float)(3.14159 / 4.), (float)((float)width / (float)height), 0.01f, 1000.0f);
///
///				render stuff
///				}
//
//			4.5 Your render function is a method!! call it from a function with the same parameter list, 
//				because we need to pass your render function as function pointer!):
//
///					Application* application = NULL; //must be global
///					void renderfct(int w, int h, glm::mat4 VRheadmatrix, int eye, bool VRon)
///						{
///						application->render_p(w, h, VRheadmatrix, eye, VRon);
///						//inside application class: 	void render_p(int width, int height,glm::mat4 VRheadmatrix,int eye,bool VRon) {...}
///						}
//
//			5. Render to VR (and screen):
///				in your main loop:
///					vrapp->render_to_VR(your_render_fct);
///					vrapp->render_to_screen(1);//0..left eye, 1..right eye
//
//
//##############################################################################################################################################################


#pragma once
#include <openvr.h>
#include <string>
#include <glm/gtc/type_ptr.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glad/glad.h>
#include "Program.h"

using namespace std;
using namespace glm;

enum emeye :int { LEFTEYE = 0, RIGHTEYE = 1, LEFTPOST = 2, RIGHTPOST = 3 };


class OpenVRApplication
{
private:
	
	Program prog;					//shader program for the postprocessing stages
	vr::TrackedDevicePose_t pose;	//matrix from the headset tracking

	void render_to_FBO(int selectFBO, void(*renderfunction)(int, int, glm::mat4,int,bool));
	unsigned int FBO[4], FBOtexture[4], FBOdepth[2];
	unsigned int  FBOvao, FBOvbopos, FBOvbotex;
	void render_to_offsetFBO(int selectFBO);

	vr::IVRSystem* hmd = NULL;
	int rtWidth = 0;
	int rtHeight = 0;

	inline static bool hmdIsPresent() { return vr::VR_IsHmdPresent(); }
	vr::TrackedDevicePose_t submitFramesOpenGL(int leftEyeTex, int rightEyeTex, bool linear = false);
	void handleVRError(vr::EVRInitError err);
	void initVR();
public:
	vec3 position=vec3(0,0,0);
	float eyeconvergence = 0.3;		// convergence point
	float eyedistance = 0.15;		//3D intesity effec
	int get_render_width() { return rtWidth; }
	int get_render_height() { return rtHeight; }
	OpenVRApplication();
	bool init_buffers(string resourceDirectory);
	bool is_VRon() { if (hmd)return true; return false; }
	bool get_projection_matrix(vr::Hmd_Eye eEye, float nearZ, float farZ, mat4 &P)
	{
		if (!hmd) return false;
		vr::HmdMatrix44_t m = hmd->GetProjectionMatrix(eEye, nearZ, farZ);
		for (int i = 0; i < 4; i++)
			for (int j = 0; j < 4; j++)
				P[j][i] = m.m[i][j];
		return true;
	}
	virtual OpenVRApplication::~OpenVRApplication()
	{
		if (hmd)
		{
			vr::VR_Shutdown();
			hmd = NULL;
		}
	}
	vr::TrackedDevicePose_t  render_to_VR(void(*renderfunction)(int, int, glm::mat4,int,bool));
	unsigned int get_FBO_texture(int i) { if (i < 0 || i>3)return 0; return FBOtexture[i]; }
	void render_to_screen(int texture_num);
};

