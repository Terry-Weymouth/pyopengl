#!/usr/bin/env python
#
#
# 3.1.3 added toggle on for shader by pressing "g" (for glsl).  Doesn't seem to
# want to toggle back off.  plVShader looks identical to phong.  To see toon
# shader change lines 163 and 164 to vShader = toonVShader
# and fShader = toonFShader
#
# 3.1.4 Attempting to add a more complex shader!  I may add some more lights
# too
# 3.1.4.1 Have multiple lights but only light0 works when shader is
# toggled on.  Check by commenting out lights in InitGL3D
#       ----------
#
from math import *
from time import sleep

from OpenGL.GL import *
from OpenGL.GL.shaders import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
from numpy import *

program = 0
vShader = None
fShader = None
myshader = "off"
shaders = ["toon", "toon2", "phong", "pl", "phongMulti"]

# ==============================================================
# Shader definitions and functions...
# ==============================================================
phongMultiVShader = [
    '''
    varying vec3 normal, eyeVec;
    #define MAX_LIGHTS 8
    #define NUM_LIGHTS 3
    varying vec3 lightDir[MAX_LIGHTS];
    void main()
    {
      gl_Position = ftransform();
      normal = gl_NormalMatrix * gl_Normal;
      vec4 vVertex = gl_ModelViewMatrix * gl_Vertex;
      eyeVec = -vVertex.xyz;
      int i;
      for (i=0; i<NUM_LIGHTS; ++i)
        lightDir[i] =
          vec3(gl_LightSource[i].position.xyz - vVertex.xyz);
}
    ''',
]

phongMultiFShader = [
    '''
    varying vec3 normal, eyeVec;
    #define MAX_LIGHTS 8
    #define NUM_LIGHTS 3
    varying vec3 lightDir[MAX_LIGHTS];
    void main (void)
    {
      vec4 final_color =
           gl_FrontLightModelProduct.sceneColor;
      vec3 N = normalize(normal);
      int i;
      for (i=0; i<NUM_LIGHTS; ++i)
      {
        vec3 L = normalize(lightDir[i]);
        float lambertTerm = dot(N,L);
        if (lambertTerm > 0.0)
        {
          final_color +=
            gl_LightSource[i].diffuse *
            gl_FrontMaterial.diffuse *
            lambertTerm;
          vec3 E = normalize(eyeVec);
          vec3 R = reflect(-L, N);
          float specular = pow(max(dot(R, E), 0.0),
                               gl_FrontMaterial.shininess);
          final_color +=
            gl_LightSource[i].specular *
            gl_FrontMaterial.specular *
            specular;
        }
      }
      gl_FragColor = final_color;
    }
    ''',
]

plVShader = [
    '''
    varying vec3 normal, lightDir, eyeVec;

    void main()
    {  
	normal = gl_NormalMatrix * gl_Normal;

	vec3 vVertex = vec3(gl_ModelViewMatrix * gl_Vertex);

	lightDir = vec3(gl_LightSource[0].position.xyz - vVertex);
	eyeVec = -vVertex;

	gl_Position = ftransform();		
    }
    ''',
]

plFShader = [
    '''
    varying vec3 normal, lightDir, eyeVec;

    void main (void)
    {
	vec4 final_color = 
	(gl_FrontLightModelProduct.sceneColor * gl_FrontMaterial.ambient) + 
	(gl_LightSource[0].ambient * gl_FrontMaterial.ambient);
							
	vec3 N = normalize(normal);
	vec3 L = normalize(lightDir);
	
	float lambertTerm = dot(N,L);
	
	if(lambertTerm > 0.0)
	{
		final_color += gl_LightSource[0].diffuse * 
		               gl_FrontMaterial.diffuse * 
					   lambertTerm;	
		
		vec3 E = normalize(eyeVec);
		vec3 R = reflect(-L, N);
		float specular = pow( max(dot(R, E), 0.0), 
		                 gl_FrontMaterial.shininess );
		final_color += gl_LightSource[0].specular * 
		               gl_FrontMaterial.specular * 
					   specular;	
	}

	gl_FragColor = final_color;			
    }
    ''',
]

# A Toon style shader (Works!)

toonVShader = [
    '''
    varying vec3 normal;
    void main() {
        normal = gl_NormalMatrix * gl_Normal;
        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    }
    ''',
]

toonFShader = [
    '''
    varying vec3 normal;
    void main() {
        float intensity;
        vec4 color;
        vec3 n = normalize(normal);
        vec3 l = normalize(gl_LightSource[0].position).xyz;

        // quantize to 10 steps 
        intensity = (floor(dot(l, n) * 9.0) + 1.0)/9.0;
        color = vec4(intensity*1.0, intensity*0.5, intensity*0.25,
            intensity*0.125);

        gl_FragColor = color;
    }
    ''',
]
# A Toon style shader (mike's version)

toon2VShader = [
    '''
    varying vec3 normal;
    void main() {
        normal = gl_NormalMatrix * gl_Normal;
        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    }
    ''',
]

toon2FShader = [
    '''
    varying vec3 normal;
    void main() {
        float intensity, intensity0, intensity1;
        vec4 color;
        vec3 n = normalize(normal);
        vec3 l0 = normalize(gl_LightSource[0].position).xyz;
        vec3 l1 = normalize(gl_LightSource[1].position).xyz;

        // quantize to 10 steps (light 0)
        intensity0 = (floor(dot(l0, n) * 9.0) + 1.0)/9.0;
        intensity1 = (floor(dot(l1, n) * 99.0) + 1.0)/99.0;
        intensity = (intensity0+intensity1)/2.0;

        color = vec4(intensity*1.0, intensity*0.5, intensity*0.25,
            intensity*0.125);

        gl_FragColor = color;
    }
    ''',
]

# A simple phong shader (not currently working)

phongVShader = [
    '''
    varying vec3 N;
    varying vec3 v;

    void main(void)  
    {     
       v = vec3(gl_ModelViewMatrix * gl_Vertex);       
       N = normalize(gl_NormalMatrix * gl_Normal);

       gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;  
    }
    ''',
]

phongFShader = [
    '''
    varying vec3 N;
    varying vec3 v;    

    void main (void)  
    {  
       vec3 L = normalize(gl_LightSource[0].position.xyz - v);   
       vec3 E = normalize(-v); // we are in Eye Coordinates, so EyePos is (0,0,0)  
       vec3 R = normalize(-reflect(L,N));  
     
       //calculate Ambient Term:  
       vec4 Iamb = gl_FrontLightProduct[0].ambient;    

       //calculate Diffuse Term:  
       vec4 Idiff = gl_FrontLightProduct[0].diffuse * max(dot(N,L), 0.0);
       Idiff = clamp(Idiff, 0.0, 1.0);     
       
       // calculate Specular Term:
       vec4 Ispec = gl_FrontLightProduct[0].specular 
                    * pow(max(dot(R,E),0.0),0.3*gl_FrontMaterial.shininess);
       Ispec = clamp(Ispec, 0.0, 1.0); 

       // write Total Color:  
       gl_FragColor = gl_FrontLightModelProduct.sceneColor + Iamb + Idiff + Ispec;     
    }
    ''',
]


# ================================
# Assign the shader to be used...
# ================================
def pickShader(direction):
    # pop a shader name from the global list and use it to put the correct shader
    # source in the text objects vShader and fShader
    global shaders, vShader, fShader, program, myshader
    if direction == "left":
        shaders.reverse()
        shaders.append(myshader)
        shaders.reverse()
        myshader = shaders.pop()
    elif direction == "right":
        shaders.append(myshader)
        myshader = shaders.pop(0)
    print("myshader = ", myshader)
    if myshader == "off":
        program = 0
    else:
        vShaderName = myshader + "VShader"
        fShaderName = myshader + "FShader"
        vShader = eval(vShaderName)
        fShader = eval(fShaderName)
        initShader()


def compileShader(source, shaderType):
    """Compile shader source of given type"""
    shader = glCreateShader(shaderType)
    # print "glShaderSource:", bool(glShaderSource)
    glShaderSource(shader, source)
    glCompileShader(shader)
    return shader


def compileProgram(vertexSource=None, fragmentSource=None):
    program = glCreateProgram()

    if vertexSource:
        vertexShader = compileShader(vertexSource, GL_VERTEX_SHADER)
        glAttachShader(program, vertexShader)
    if fragmentSource:
        fragmentShader = compileShader(fragmentSource, GL_FRAGMENT_SHADER)
        glAttachShader(program, fragmentShader)

    glValidateProgram(program)
    glLinkProgram(program)

    if vertexShader:
        glDeleteShader(vertexShader)
    if fragmentShader:
        glDeleteShader(fragmentShader)

    return program


def initShader():
    global program
    program = compileProgram(vShader, fShader)


# ===================================================

# Handle key press events 
def keyPressed(*args):
    print("key = ", args)
    # note shaderNumber still not in use
    global rotate, wireframe, solid, normave, shaderOn, \
        shaderNumber, light0, light1
    ESCAPE = b'\x1b'
    # If escape is pressed, kill everything.
    if args[0] == ESCAPE:
        print("Exit")
        sys.exit(0)
    # toggle rotation
    elif args[0] == b'r':
        if rotate != True:
            rotate = True
        else:
            rotate = False
        print("rotate =", rotate)
    # toggle wireframe
    elif args[0] == b'w':
        if wireframe != True:
            wireframe = True
        else:
            wireframe = False
        print("wireframe =", wireframe)
    # toggle solid
    elif args[0] == b's':
        if solid != True:
            solid = True
        else:
            solid = False
        print("solid =", solid)
    # toggle average normals
    elif args[0] == b'n':
        if normave != True:
            normave = True
        else:
            normave = False
        print("normave =", normave)
    # toggle shader on
    elif args[0] == b'g':
        if shaderOn != True:
            shaderOn = True
        else:
            shaderOn = False
        print("shaderOn =", shaderOn)
    # toggle light 1
    elif args[0] == b'1':
        if light0 != True:
            light0 = True
        else:
            light0 = False
    # toggle light 2
    elif args[0] == b'2':
        if light1 != True:
            light1 = True
        else:
            light1 = False
    # change shader
    elif args[0] == b',':
        pickShader("left")
        print("shader = left")
    elif args[0] == b'.':
        pickShader("right")
        print("shader = right")


def initLight0():
    LightAmbient = ((0.0, 0.0, 0.0, 1.0))
    LightDiffuse = ((0.5, 0.5, 0.5, 1.0))
    LightPosition = ((1200.0, 1000.0, 1000.0, 1.0))
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glLightfv(GL_LIGHT0, GL_AMBIENT, LightAmbient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, LightDiffuse)
    glLightfv(GL_LIGHT0, GL_POSITION, LightPosition)
    glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, [.2, .2, .2, 1])
    glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, 0.5)
    glMaterial(GL_FRONT_AND_BACK, GL_EMISSION, [.2, .2, .2, 1])
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)


def initLight1():
    LightAmbient = ((1.0, 0.0, 0.0, 1.0))
    LightDiffuse = ((1.0, 0.5, 0.5, 1.0))
    LightPosition = ((400.0, 8000.0, 5000.0, 1.0))
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glLightfv(GL_LIGHT1, GL_AMBIENT, LightAmbient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, LightDiffuse)
    glLightfv(GL_LIGHT1, GL_POSITION, LightPosition)
    glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, [.2, .2, .2, 1])
    glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, 64.0)
    glMaterial(GL_FRONT_AND_BACK, GL_EMISSION, [.2, .2, .2, 1])
    # glEnable (GL_COLOR_MATERIAL)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHTING)


# Initialize the OpenGL window using 3D perspective projection
def InitGL3D(Width, Height):
    # Setup a 2D projection
    global zdist
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClearDepth(1.0)
    initLight0()
    initLight1()
    # lighting option
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    viewangle = 15.0
    zdist = Width / (2 * (tan(radians(viewangle / 2))))
    print("zdist = ", zdist)
    gluPerspective(viewangle, float(Width) / float(Height), zdist - 600.0, zdist + 600.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glLineWidth(0.1)
    glTranslatef(-200, 0, -zdist)
    glRotate(180.0, 1.0, 0.0, 0.0)
    glColor(176. / 255., 146. / 255., 113. / 255.)
    # Initialize the Shader(s)!!!?
    # initShader()
    # Initialize buffer objects for vertices and normal array data
    initVBOs()


# Create and fill vbo type buffer objects
def initVBOs():
    global vertvbo, flatvbo, avevbo
    # vertices
    vertvbo = vbo.VBO(array(modelverts, 'f'))
    # flat normals
    flatvbo = vbo.VBO(array(flatnorms, 'f'))
    # average(smooth) normals
    avevbo = vbo.VBO(array(avenorms, 'f'))


# ================================================
# Draw the scene.  Draw a glutSolidSphere and 
# draw a shape from the a gmsh triangle array
# ================================================
def drawScene():
    glEnable(GL_LIGHTING)
    if light0:
        glEnable(GL_LIGHT0)
    else:
        glDisable(GL_LIGHT0)
    if light1:
        glEnable(GL_LIGHT1)
    else:
        glDisable(GL_LIGHT1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor4f(1.0, 1.0, 1.0, 1.0)
    # Enable Shader Program
    glUseProgram(program)
    # Draw OUR SPHERE (complete with normals calculated in getGmshModel)
    if solid:
        glColor4f(0.1, 0.1, 1.0, 1.0)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glutSolidSphere(150.0, 24, 24)
        vertvbo.bind()
        glVertexPointerf(vertvbo)
        if not normave:
            flatvbo.bind()
            glNormalPointerf(flatvbo)
        else:
            avevbo.bind()
            glNormalPointerf(avevbo)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glDrawArrays(GL_TRIANGLES, 0, len(modelverts))
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
    # Turn off the shader program for wireframe and text rendering
    glUseProgram(0)
    # draw the triangle edges
    if wireframe:
        glDisable(GL_LIGHTING)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glutSolidSphere(150.0, 24, 24)
        glEnableClientState(GL_VERTEX_ARRAY)
        glDrawArrays(GL_TRIANGLES, 0, len(modelverts))
        glDisableClientState(GL_VERTEX_ARRAY)
    if rotate:
        glRotate(2.0, 0.0, 1.0, 0.0)
    # put some notes on the screen
    if not normave:
        normtext = "flat"
    else:
        normtext = "averaged"
    infotext = "Shader: " + myshader + "     Gmsh Normals: " + normtext
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_LIGHTING)
#    drawGLtext(labeltext, -320, -220)
#    drawGLtext(infotext, -300, -400)
    glPopMatrix()
    glutSwapBuffers()
    sleep(0.04)


# Draw text in the GL window
# def drawGLtext(text, tx, ty):
#     textcolor = [1, 1, 1]
#     colR = textcolor[0]
#     colG = textcolor[1]
#     colB = textcolor[2]
#     glColor3f(colR, colG, colB)
#     glRasterPos3f(tx, ty, -zdist)
#     for char in text:
#         if char == "\n":
#             ty += 20
#             glRasterPos3f(tx, ty, -zdist)
#         else:
#             glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))


# read in the gmsh triangle element file and create a vertex array
def getGmshModel(gmshfile, scale, dx, dy, dz):
    print(gmshfile)
    infile = open('./sphere1218.msh', 'r')
    gmshlines = infile.readlines()
    # read in the nodes and triangles
    readnodes = False
    readelems = False
    skipline = 0
    elems = []
    lnum = 0
    nnodes = 0
    for line in gmshlines:
        if "$Nodes" in line:
            readnodes = True
            skipline = 2
            nnodes = int(gmshlines[lnum + 1].strip())
            nodes = []
            for i in range(nnodes):
                nodes.append(99999.9)
        elif "$EndNodes" in line:
            readnodes = False
            skipline = 1
        elif "$Elements" in line:
            readelems = True
            skipline = 2
        elif "$EndElements" in line:
            readelems = False
            skipline = 1
        if skipline < 1:
            if readnodes:
                nXYZ = line.strip().split()
                nodenum = int(nXYZ[0]) - 1
                nX = float(nXYZ[1]) * scale + dx
                nY = float(nXYZ[2]) * scale + dy
                nZ = float(nXYZ[3]) * scale + dz
                nodes[nodenum] = [nX, nY, nZ]
            elif readelems:
                n123 = line.split()
                if n123[1] == "2":
                    n1 = int(n123[-3]) - 1
                    n2 = int(n123[-1]) - 1
                    n3 = int(n123[-2]) - 1
                    elems.append([n1, n2, n3])
        else:
            skipline -= 1
        lnum += 1
    # generate the triangle array from the elements and nodes
    # (need to work on sorting things for speed later)
    triarray = []
    normarray = []
    avenorms = []
    # generate the average normal array
    nodeavenorms = getAveNormals(nodes, elems)
    for elem in elems:
        # temporarily store the vertices locations
        vert1 = [nodes[elem[0]][0], nodes[elem[0]][1], nodes[elem[0]][2]]
        vert2 = [nodes[elem[1]][0], nodes[elem[1]][1], nodes[elem[1]][2]]
        vert3 = [nodes[elem[2]][0], nodes[elem[2]][1], nodes[elem[2]][2]]
        avenorm0 = nodeavenorms[elem[0]]
        avenorm1 = nodeavenorms[elem[1]]
        avenorm2 = nodeavenorms[elem[2]]
        # calculate the triangle normal (right handed, 1-2 2-3)
        normals = getNormals(vert1, vert2, vert3)
        triarray.append(vert1)
        triarray.append(vert2)
        triarray.append(vert3)
        # assign the triangle normal to all three vertices
        normarray.append(normals)
        normarray.append(normals)
        normarray.append(normals)
        # assign the average normal to each vertex
        avenorms.append(avenorm0)
        avenorms.append(avenorm1)
        avenorms.append(avenorm2)
    # return the triangle and normal arrays
    return triarray, normarray, avenorms


# calculate the average normals for each vertex associated with
# multiple triangles
def getAveNormals(nodes, elems):
    nodetrilist = []
    # load a list with all of the elements that share a node
    for nodenum in range(len(nodes)):
        nodetrilist.append([])
        for elemnum in range(len(elems)):
            if nodenum in elems[elemnum]:
                nodetrilist[nodenum].append(elemnum)
    # get the normals for each element attached to each node
    avenorms = []
    for tri in nodetrilist:
        aveNi = 0.0
        aveNj = 0.0
        aveNk = 0.0
        denom = max(float(len(tri)), 1)
        for elem in tri:
            # load the vertices for each element
            vert1 = [nodes[elems[elem][0]][0], nodes[elems[elem][0]][1], nodes[elems[elem][0]][2]]
            vert2 = [nodes[elems[elem][1]][0], nodes[elems[elem][1]][1], nodes[elems[elem][1]][2]]
            vert3 = [nodes[elems[elem][2]][0], nodes[elems[elem][2]][1], nodes[elems[elem][2]][2]]
            # calculate the normal and add each component to the total
            normals = getNormals(vert1, vert2, vert3)
            aveNi += normals[0]
            aveNj += normals[1]
            aveNk += normals[2]
        # divide by the number of elements and append to the array
        avenorms.append([aveNi / denom, aveNj / denom, aveNk / denom])
    return avenorms


# calculate the normal from three vertex locations
def getNormals(vertA, vertB, vertC):
    # store vertex x-y-z locations
    xA = vertA[0]
    xB = vertB[0]
    xC = vertC[0]
    yA = vertA[1]
    yB = vertB[1]
    yC = vertC[1]
    zA = vertA[2]
    zB = vertB[2]
    zC = vertC[2]
    # define the vector components from A-B and B-C
    ABx = xB - xA
    ABy = yB - yA
    ABz = zB - zA
    BCx = xC - xB
    BCy = yC - yB
    BCz = zC - zB
    # take the cross product AB X BC to get the dimensional normal vector
    Nx = ABy * BCz - ABz * BCy
    Ny = ABz * BCx - ABx * BCz
    Nz = ABx * BCy - ABy * BCx
    # nondimensionalize (make a unit vector)
    VecMag = sqrt(Nx ** 2 + Ny ** 2 + Nz ** 2)
    Ni = Nx / VecMag
    Nj = Ny / VecMag
    Nk = Nz / VecMag
    # return the normal vector
    return [Ni, Nj, Nk]


# write the converted gmsh geometry out to a file that can be
# used as an asset in the game engine
def writemodel():
    modelname = gmshmodel.replace(".msh", ".dustmodel")
    modelout = open(modelname, 'w')
    # write out the vertices
    modelout.write("Dust Engine Model\nVersion\n0.1\n")
    modelout.write("VERTICES\n")
    modelout.write(str(len(modelverts)) + "\n")
    for vert in modelverts:
        modelout.write(str(vert).replace("[", "").replace("]", "") + "\n")
    modelout.write("FLAT NORMALS\n")
    modelout.write(str(len(flatnorms)) + "\n")
    for norm in flatnorms:
        modelout.write(str(norm).replace("[", "").replace("]", "") + "\n")
    modelout.write("SMOOTH NORMALS\n")
    modelout.write(str(len(avenorms)) + "\n")
    for norm in flatnorms:
        modelout.write(str(norm).replace("[", "").replace("]", "") + "\n")
    modelout.close()


# Main graphics function
def gl_main():
    global Width, Height
    glutInit(sys.argv)
    glutCreateWindow("GMSH Model Render Test 1 - Mike & Matt 2011")
    glutReshapeWindow(Width, Height)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_ALPHA)
    glutInitWindowPosition(0, 0)

    # Set the default glut display function
    glutDisplayFunc(drawScene)

    # Set the idle function
    glutIdleFunc(drawScene)

    # Uncomment this line to get full screen.
    # glutFullScreen()

    # Initialize our window.
    InitGL3D(Width, Height)

    # Register the function called when the keyboard is pressed.
    glutKeyboardFunc(keyPressed)

    # Start Event Processing Engine
    glutMainLoop()


# Main Program
# set some default values
Width = 864
Height = 600
wireframe = False
solid = True
rotate = False
firstrun = True
trinum = 0
normave = False
shaderOn = False
light0 = True
light1 = True
gmshmodel = "sphere1218.msh"
scale = 300.0
dx = 400.0
dy = 0.0
dz = 0.0
modelverts, flatnorms, avenorms = getGmshModel(gmshmodel, scale, dx, dy, dz)

print("generated ", len(modelverts) / 3, " triangles from ", gmshmodel)

writemodel()

labeltext = "glutSolidSphere                     Gmsh " + gmshmodel.replace(".msh", "")

# =====================
# Initialize Main loop
# =====================

gl_main()
