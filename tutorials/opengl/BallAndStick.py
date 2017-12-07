#
# Based on and modified from Lesson5.py from...
# Many changes - the lesson source was just a place for me to start. Other information sources used:
#
# 
# Provenance:
# downloaded from: https://code.launchpad.net/~mcfletch/pyopengl-demo/trunk (Dec 2017)
# Ported to PyOpenGL 2.0 by Tarn Weisner Burton 10May2001
# This code was created by Richard Campbell '99 (ported to Python/PyOpenGL by John Ferguson 2000)
# The port was based on the PyOpenGL tutorial module: dots.py
# If you've found this code useful, please let me know (email John Ferguson at hakuin@voicenet.com).
# See original source and C based tutorial at http://nehe.gamedev.net
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = b'\x1b'

# Number of the glut window.
window = 0

# Rotation angle for the triangle. 
rtri = 0.0

# Rotation angle for the quadrilateral.
rquad = 0.0


# A general OpenGL initialization function.  Sets all of the initial parameters.
def init_gl(width, height):  # We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)  # This Will Clear The Background Color To Black
    glClearDepth(1.0)  # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)  # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)  # Enables Depth Testing
    glShadeModel(GL_SMOOTH)  # Enables Smooth Color Shading

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # Reset The Projection Matrix
    # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)


# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def resize_gl_scene(width, height):
    if height == 0:  # Prevent A Divide By Zero If The Window Is Too Small
        height = 1

    glViewport(0, 0, width, height)  # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


# The main drawing function.
def draw_gl_scene():
    global rtri, rquad

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear The Screen And The Depth Buffer
    # glLoadIdentity()  # Reset The View
    # glTranslatef(-0.9, 0.0, -6.0)  # Move Left And Into The Screen
    #
    # glRotatef(rtri, math.cos(rtri), math.sin(rtri), 0.5)  # Rotate The Pyramid
    #
    # glBegin(GL_TRIANGLES)  # Start Drawing The Pyramid
    #
    # glColor3f(1.0, 0.0, 0.0)  # Red
    # glVertex3f(0.0, 1.0, 0.0)  # Top Of Triangle (Front)
    # glColor3f(0.0, 1.0, 0.0)  # Green
    # glVertex3f(-1.0, -1.0, 1.0)  # Left Of Triangle (Front)
    # glColor3f(0.0, 0.0, 1.0)  # Blue
    # glVertex3f(1.0, -1.0, 1.0)
    #
    # glColor3f(1.0, 0.0, 0.0)  # Red
    # glVertex3f(0.0, 1.0, 0.0)  # Top Of Triangle (Right)
    # glColor3f(0.0, 0.0, 1.0)  # Blue
    # glVertex3f(1.0, -1.0, 1.0)  # Left Of Triangle (Right)
    # glColor3f(0.0, 1.0, 0.0)  # Green
    # glVertex3f(1.0, -1.0, -1.0)  # Right
    #
    # glColor3f(1.0, 0.0, 0.0)  # Red
    # glVertex3f(0.0, 1.0, 0.0)  # Top Of Triangle (Back)
    # glColor3f(0.0, 1.0, 0.0)  # Green
    # glVertex3f(1.0, -1.0, -1.0)  # Left Of Triangle (Back)
    # glColor3f(0.0, 0.0, 1.0)  # Blue
    # glVertex3f(-1.0, -1.0, -1.0)  # Right Of Triangle (Back)
    #
    # glColor3f(1.0, 0.0, 0.0)  # Red
    # glVertex3f(0.0, 1.0, 0.0)  # Top Of Triangle (Left)
    # glColor3f(0.0, 0.0, 1.0)  # Blue
    # glVertex3f(-1.0, -1.0, -1.0)  # Left Of Triangle (Left)
    # glColor3f(0.0, 1.0, 0.0)  # Green
    # glVertex3f(-1.0, -1.0, 1.0)  # Right Of Triangle (Left)
    # glEnd()

    glLoadIdentity()
    glTranslatef(0.9, 0.0, -6.0)  # Move Right And Into The Screen
    glRotatef(rquad, 1.0, 1.0, 1.0)  # Rotate The Cube On X, Y & Z
    glBegin(GL_QUADS)  # Start Drawing The Cube

    glColor3f(0.0, 1.0, 0.0)  # Set The Color To Blue
    glVertex3f(1.0, 1.0, -1.0)  # Top Right Of The Quad (Top)
    glVertex3f(-1.0, 1.0, -1.0)  # Top Left Of The Quad (Top)
    glVertex3f(-1.0, 1.0, 1.0)  # Bottom Left Of The Quad (Top)
    glVertex3f(1.0, 1.0, 1.0)  # Bottom Right Of The Quad (Top)

    glColor3f(1.0, 0.5, 0.0)  # Set The Color To Orange
    glVertex3f(1.0, -1.0, 1.0)  # Top Right Of The Quad (Bottom)
    glVertex3f(-1.0, -1.0, 1.0)  # Top Left Of The Quad (Bottom)
    glVertex3f(-1.0, -1.0, -1.0)  # Bottom Left Of The Quad (Bottom)
    glVertex3f(1.0, -1.0, -1.0)  # Bottom Right Of The Quad (Bottom)

    glColor3f(1.0, 0.0, 0.0)  # Set The Color To Red
    glVertex3f(1.0, 1.0, 1.0)  # Top Right Of The Quad (Front)
    glVertex3f(-1.0, 1.0, 1.0)  # Top Left Of The Quad (Front)
    glVertex3f(-1.0, -1.0, 1.0)  # Bottom Left Of The Quad (Front)
    glVertex3f(1.0, -1.0, 1.0)  # Bottom Right Of The Quad (Front)

    glColor3f(1.0, 1.0, 0.0)  # Set The Color To Yellow
    glVertex3f(1.0, -1.0, -1.0)  # Bottom Left Of The Quad (Back)
    glVertex3f(-1.0, -1.0, -1.0)  # Bottom Right Of The Quad (Back)
    glVertex3f(-1.0, 1.0, -1.0)  # Top Right Of The Quad (Back)
    glVertex3f(1.0, 1.0, -1.0)  # Top Left Of The Quad (Back)

    glColor3f(0.0, 0.0, 1.0)  # Set The Color To Blue
    glVertex3f(-1.0, 1.0, 1.0)  # Top Right Of The Quad (Left)
    glVertex3f(-1.0, 1.0, -1.0)  # Top Left Of The Quad (Left)
    glVertex3f(-1.0, -1.0, -1.0)  # Bottom Left Of The Quad (Left)
    glVertex3f(-1.0, -1.0, 1.0)  # Bottom Right Of The Quad (Left)

    glColor3f(1.0, 0.0, 1.0)  # Set The Color To Violet
    glVertex3f(1.0, 1.0, -1.0)  # Top Right Of The Quad (Right)
    glVertex3f(1.0, 1.0, 1.0)  # Top Left Of The Quad (Right)
    glVertex3f(1.0, -1.0, 1.0)  # Bottom Left Of The Quad (Right)
    glVertex3f(1.0, -1.0, -1.0)  # Bottom Right Of The Quad (Right)
    glEnd()  # Done Drawing The Quad

    glLoadIdentity()  # Reset The View
    glScalef(0.1, 0.1, 0.1)
    glTranslatef(-0.9, 0.0, -6.0)  # Move Left And Into The Screen

    glRotatef(rtri, math.cos(rtri), math.sin(rtri), 0.5)  # Rotate The Pyramid

    glColor3f(1.0, 0.0, 1.0)

    glutSolidDodecahedron()

    # What values to use?  Well, if you have a FAST machine and a FAST 3D Card, then
    # large values make an unpleasant display with flickering and tearing.  I found that
    # smaller values work better, but this was based on my experience.
    rtri = rtri + 0.05  # Increase The Rotation Variable For The Triangle
    rquad = rquad - 0.15  # Decrease The Rotation Variable For The Quad

    #  since this is double buffered, swap the buffers to display what just got drawn.
    glutSwapBuffers()


# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
def key_pressed(*args):
    # If escape is pressed, kill everything.
    if args[0] == ESCAPE:
        sys.exit()


def main():
    global window
    glutInit(sys.argv)

    # Select type of Display mode:
    #  Double buffer
    #  RGBA color
    # Alpha components supported
    # Depth buffer
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    # get a 640 x 480 window
    glutInitWindowSize(640, 480)

    # the window starts at the upper left corner of the screen
    glutInitWindowPosition(0, 0)

    # Okay, like the C version we retain the window id to use when closing, but for those of you new
    # to Python (like myself), remember this assignment would make the variable local and not global
    # if it weren't for the global declaration at the start of main.
    window = glutCreateWindow("Jeff Molofee's GL Code Tutorial ... NeHe '99")

    # Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
    # set the function pointer and invoke a function to actually register the callback, otherwise it
    # would be very much like the C version of the code.
    glutDisplayFunc(draw_gl_scene)

    # Uncomment this line to get full screen.
    # glutFullScreen()

    # When we are doing nothing, redraw the scene.
    glutIdleFunc(draw_gl_scene)

    # Register the function called when our window is resized.
    glutReshapeFunc(resize_gl_scene)

    # Register the function called when the keyboard is pressed.
    glutKeyboardFunc(key_pressed)

    # Initialize our window.
    init_gl(640, 480)

    # Start Event Processing Engine
    glutMainLoop()

# def draw_sphere():
#
#     glBegin(GL_TRIANGLE_FAN)
#     # create 12 vertices of an icosahedron
#     t = (1.0 + math.sqrt(5.0)) / 2.0
#
#     addVertex(-1,  t,  0)
#     addVertex( 1,  t,  0)
#     addVertex(-1, -t,  0)
#     addVertex( 1, -t,  0)
#
#     addVertex( 0, -1,  t)
#     addVertex( 0,  1,  t)
#     addVertex( 0, -1, -t)
#     addVertex( 0,  1, -t)
#
#     addVertex( t,  0, -1)
#     addVertex( t,  0,  1)
#     addVertex(-t,  0, -1)
#     addVertex(-t,  0,  1)
#
#     # create 20 triangles of the icosahedron
#     faces = []
#
#     # 5 faces around point 0
#     faces.Add(new TriangleIndices(0, 11, 5))
#     faces.Add(new TriangleIndices(0, 5, 1))
#     faces.Add(new TriangleIndices(0, 1, 7))
#     faces.Add(new TriangleIndices(0, 7, 10))
#     faces.Add(new TriangleIndices(0, 10, 11))
#
#     # 5 adjacent faces
#     faces.Add(new TriangleIndices(1, 5, 9))
#     faces.Add(new TriangleIndices(5, 11, 4))
#     faces.Add(new TriangleIndices(11, 10, 2))
#     faces.Add(new TriangleIndices(10, 7, 6))
#     faces.Add(new TriangleIndices(7, 1, 8))
#
#     # 5 faces around point 3
#     faces.Add(new TriangleIndices(3, 9, 4))
#     faces.Add(new TriangleIndices(3, 4, 2))
#     faces.Add(new TriangleIndices(3, 2, 6))
#     faces.Add(new TriangleIndices(3, 6, 8))
#     faces.Add(new TriangleIndices(3, 8, 9))
#
#     # 5 adjacent faces
#     faces.Add(new TriangleIndices(4, 9, 5))
#     faces.Add(new TriangleIndices(2, 4, 11))
#     faces.Add(new TriangleIndices(6, 2, 10))
#     faces.Add(new TriangleIndices(8, 6, 7))
#     faces.Add(new TriangleIndices(9, 8, 1))

# Print message to console, and kick off the main to get it rolling.
print("Hit ESC key to quit.")
main()
