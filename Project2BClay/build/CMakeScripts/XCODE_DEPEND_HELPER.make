# DO NOT EDIT
# This makefile makes sure all linkable targets are
# up-to-date with anything they link to
default:
	echo "Do not invoke directly"

# Rules to remove targets that are older than anything to which they
# link.  This forces Xcode to relink the targets from scratch.  It
# does not seem to check these dependencies itself.
PostBuild.glfw.Debug:
/Library/OpenGL_MAC/glfw-mojave-fixes/debug/src/Debug/libglfw3.a:
	/bin/rm -f /Library/OpenGL_MAC/glfw-mojave-fixes/debug/src/Debug/libglfw3.a


PostBuild.proj2.Debug:
PostBuild.glfw.Debug: /Users/clayrosenthal/Git/csc471F19/Project2BClay/build/Debug/proj2
/Users/clayrosenthal/Git/csc471F19/Project2BClay/build/Debug/proj2:\
	/Library/OpenGL_MAC/glfw-mojave-fixes/debug/src/Debug/libglfw3.a
	/bin/rm -f /Users/clayrosenthal/Git/csc471F19/Project2BClay/build/Debug/proj2


PostBuild.glfw.Release:
/Library/OpenGL_MAC/glfw-mojave-fixes/debug/src/Release/libglfw3.a:
	/bin/rm -f /Library/OpenGL_MAC/glfw-mojave-fixes/debug/src/Release/libglfw3.a


PostBuild.proj2.Release:
PostBuild.glfw.Release: /Users/clayrosenthal/Git/csc471F19/Project2BClay/build/Release/proj2
/Users/clayrosenthal/Git/csc471F19/Project2BClay/build/Release/proj2:\
	/Library/OpenGL_MAC/glfw-mojave-fixes/debug/src/Release/libglfw3.a
	/bin/rm -f /Users/clayrosenthal/Git/csc471F19/Project2BClay/build/Release/proj2


PostBuild.glfw.MinSizeRel:
/Library/OpenGL_MAC/glfw-mojave-fixes/debug/src/MinSizeRel/libglfw3.a:
	/bin/rm -f /Library/OpenGL_MAC/glfw-mojave-fixes/debug/src/MinSizeRel/libglfw3.a


PostBuild.proj2.MinSizeRel:
PostBuild.glfw.MinSizeRel: /Users/clayrosenthal/Git/csc471F19/Project2BClay/build/MinSizeRel/proj2
/Users/clayrosenthal/Git/csc471F19/Project2BClay/build/MinSizeRel/proj2:\
	/Library/OpenGL_MAC/glfw-mojave-fixes/debug/src/MinSizeRel/libglfw3.a
	/bin/rm -f /Users/clayrosenthal/Git/csc471F19/Project2BClay/build/MinSizeRel/proj2


PostBuild.glfw.RelWithDebInfo:
/Library/OpenGL_MAC/glfw-mojave-fixes/debug/src/RelWithDebInfo/libglfw3.a:
	/bin/rm -f /Library/OpenGL_MAC/glfw-mojave-fixes/debug/src/RelWithDebInfo/libglfw3.a


PostBuild.proj2.RelWithDebInfo:
PostBuild.glfw.RelWithDebInfo: /Users/clayrosenthal/Git/csc471F19/Project2BClay/build/RelWithDebInfo/proj2
/Users/clayrosenthal/Git/csc471F19/Project2BClay/build/RelWithDebInfo/proj2:\
	/Library/OpenGL_MAC/glfw-mojave-fixes/debug/src/RelWithDebInfo/libglfw3.a
	/bin/rm -f /Users/clayrosenthal/Git/csc471F19/Project2BClay/build/RelWithDebInfo/proj2




# For each target create a dummy ruleso the target does not have to exist
/Library/OpenGL_MAC/glfw-mojave-fixes/debug/src/Debug/libglfw3.a:
/Library/OpenGL_MAC/glfw-mojave-fixes/debug/src/MinSizeRel/libglfw3.a:
/Library/OpenGL_MAC/glfw-mojave-fixes/debug/src/RelWithDebInfo/libglfw3.a:
/Library/OpenGL_MAC/glfw-mojave-fixes/debug/src/Release/libglfw3.a:
