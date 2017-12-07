import pygame
from OpenGL.GL import glBegin, glEnd, glVertex3fv, glTranslatef, glClear, glRotatef
from OpenGL.GL import GL_LINES, GL_DOUBLEBUFFER, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
from OpenGL.GLU import *

vertices = (
    ( 1, -1, -1),
    ( 1,  1, -1),
    (-1,  1, -1),
    (-1, -1, -1),
    ( 1, -1,  1),
    ( 1,  1,  1),
    (-1, -1,  1),
    (-1,  1,  1)
)

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,6),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
)

def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def main():
    pygame.init()
    display = (800,600)
#    pygame.display.set_mode(display, pygame.DOUBLEBUFFER)

    screen = pygame.display.set_mode(display)

    gluPerspective(45, display[0]/display[1], 0.001, 1000.0)

    glTranslatef(0.0,0.0,-5.0)

    glRotatef(0,0,0,0)

    print ('before loop')
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)

    print ('after loop')

main()

