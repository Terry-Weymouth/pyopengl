#! /usr/bin/env python
'''Tests rendering using shader objects from core GL or extensions

Uses the:
    Lighthouse 3D Tutorial toon shader
        http://www.lighthouse3d.com/opengl/glsl/index.php?toon2

By way of:
    http://www.pygame.org/wiki/GLSLExample
'''
print('Starting')
import OpenGL

OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# PyOpenGL 3.0.1 introduces this convenience module...
from OpenGL.GL.shaders import *

import sys

program = None
rot = 0.0


# A general OpenGL initialization function.  Sets all of the initial parameters.
def InitGL(Width, Height):  # We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)  # This Will Clear The Background Color To Black
    glClearDepth(1.0)  # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)  # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)  # Enables Depth Testing
    glShadeModel(GL_SMOOTH)  # Enables Smooth Color Shading

    glEnable(GL_CULL_FACE)  # back-face culling

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # Reset The Projection Matrix
    # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)

    if not glUseProgram:
        print('Missing Shader Objects!')
        sys.exit(1)
    global program
    program = compileProgram(
        compileShader('''
            varying vec3 normal;
            void main() {
                normal = gl_NormalMatrix * gl_Normal;
                gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
            }
        ''', GL_VERTEX_SHADER),
        compileShader('''
            varying vec3 normal;
            void main() {
                float intensity;
                vec4 color;
                vec3 n = normalize(normal);
                vec3 l = normalize(gl_LightSource[0].position).xyz;

                // quantize to 5 steps (0, .25, .5, .75 and 1)
                // intensity = (floor(dot(l, n) * 4.0) + 1.0)/4.0;
                intensity = dot(l, n);
                color = vec4(intensity*1.0, intensity*1.0, intensity*0.8,
                    intensity*1.0);

                gl_FragColor = color;
            }
    ''', GL_FRAGMENT_SHADER), )


# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:  # Prevent A Divide By Zero If The Window Is Too Small
        Height = 1

    glViewport(0, 0, Width, Height)  # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


# The main drawing function.
def DrawGLScene():
    global rot
    stick_r = 0.08

    # Clear The Screen And The Depth Buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset The View
    if program:
        glUseProgram(program)

    rot += 2.0
    glTranslatef(0.0, 0.0, -20.0)
    glRotatef(rot, 0, 1.0, 0.1)

    dumb_bell_lattice(stick_r)

    glTranslatef(0.5, 0.5, 0.5)
    dumb_bell_lattice(stick_r)
    glTranslatef(-0.5, -0.5, -0.5)

    glTranslatef(0.0, 0.0, 2.0)

    dumb_bell_lattice(stick_r)

    glTranslatef(0.5, 0.5, 0.5)
    dumb_bell_lattice(stick_r)
    glTranslatef(-0.5, -0.5, -0.5)

    glTranslatef(0.0, 0.0, 2.0)

    dumb_bell_lattice(stick_r)

    glTranslatef(0.5, 0.5, 0.5)
    dumb_bell_lattice(stick_r)
    glTranslatef(-0.5, -0.5, -0.5)

    glTranslatef(0.0, 0.0, 2.0)

    dumb_bell_lattice(stick_r)

    glTranslatef(0.5, 0.5, 0.5)
    dumb_bell_lattice(stick_r)
    glTranslatef(-0.5, -0.5, -0.5)

    glTranslatef(0.0, 0.0, 2.0)

    dumb_bell_lattice(stick_r)

    glTranslatef(0.5, 0.5, 0.5)
    dumb_bell_lattice(stick_r)
    glTranslatef(-0.5, -0.5, -0.5)

    #  since this is double buffered, swap the buffers to display what just got drawn.
    glutSwapBuffers()

def dumb_bell_lattice(stick_r):
    glTranslate(-5, -5, 0)

    # dumb-bell lattice
    for ix in range(0,10):
        x = float(ix)
        glTranslate(x,0,0)
        for iy in range(0,10):
            y = float(iy)
            glTranslate(0, y, 0)
            glTranslatef(0.0, 0.0, -0.8)
            glutSolidSphere(0.2, 32, 32)
            cylinder(stick_r, 1.2)
            glTranslatef(0.0, 0.0, 1.2)
            glutSolidSphere(0.2, 32, 32)
            glTranslatef(0.0, 0.0, -1.2)
            glTranslatef(0.0, 0.0,  0.8)
            glTranslate(0, -y, 0)
        glTranslate(-x, 0, 0)

    glTranslate(5, 5, 0)

    glTranslate(-5, -5, 0)

    for ix in range(0,9):
        x = float(ix)
        glTranslate(x,0,0)
        for iy in range(0,10):
            y = float(iy)
            glTranslate(0, y, 0)
            glTranslate(0, 0, 0.4)
            glRotate(90, 0, 1, 0)
            cylinder(stick_r, 1)
            glRotate(-90, 0, 1, 0)
            glTranslate(0, 0, -0.4)

            glTranslate(0, 0, -0.8)
            glRotate(90, 0, 1, 0)
            cylinder(stick_r, 1)
            glRotate(-90, 0, 1, 0)
            glTranslate(0, 0, 0.8)
            glTranslate(0, -y, 0)
        glTranslate(-x, 0, 0)

    glTranslate(5, 5, 0)

    glTranslate(-5, -5, 0)

    for ix in range(0,10):
        x = float(ix)
        glTranslate(x,0,0)
        for iy in range(0,9):
            y = float(iy)
            glTranslate(0, y, 0)
            glTranslate(0, 0, 0.4)
            glRotate(-90, 1, 0, 0)
            cylinder(stick_r, 1)
            glRotate(90, 1, 0, 0)
            glTranslate(0, 0, -0.4)

            glTranslate(0, 0, -0.8)
            glRotate(-90, 1, 0, 0)
            cylinder(stick_r, 1)
            glRotate(90, 1, 0, 0)
            glTranslate(0, 0, 0.8)
            glTranslate(0, -y, 0)
        glTranslate(-x, 0, 0)

    glTranslate(5, 5, 0)


def cylinder(r, h):
    quadratic = gluNewQuadric()
    # gluCylinder(quadratic, RADIUS_BASE, RADIUS_TOP, HEIGHT, SLICES, STACKS)  # to draw the lateral parts of the cylinder;
    gluCylinder(quadratic, r, r, h, 32, 4)
    #  gluDisk(quadratic, INNER_RADIUS, OUTER_RADIUS, SLICES, LOOPS)
    glRotatef(180, 0, 1.0, 0)
    gluDisk(quadratic, 0.0, r, 32, 2)
    glRotatef(-180, 0, 1.0, 0)
    glTranslate(0, 0, h)
    gluDisk(quadratic, 0.0, r, 32, 2)
    glTranslate(0, 0, -h)


# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
def keyPressed(*args):
    # If escape is pressed, kill everything.
    if args[0] == b'\x1b':
        sys.exit()


def main():
    print('Main')
    global window
    # For now we just pass glutInit one empty argument. I wasn't sure what should or could be passed in (tuple, list, ...)
    # Once I find out the right stuff based on reading the PyOpenGL source, I'll address this.
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
    glutDisplayFunc(DrawGLScene)

    # Uncomment this line to get full screen.
    # glutFullScreen()

    # When we are doing nothing, redraw the scene.
    glutIdleFunc(DrawGLScene)

    # Register the function called when our window is resized.
    glutReshapeFunc(ReSizeGLScene)

    # Register the function called when the keyboard is pressed.
    glutKeyboardFunc(keyPressed)

    # Initialize our window.
    InitGL(640, 480)

    # Start Event Processing Engine
    print('Mainloop starting')
    glutMainLoop()


# Print message to console, and kick off the main to get it rolling.

if __name__ == "__main__":
    print("Hit ESC key to quit.")
    main()
