render = ez.Node()
aspect2D = ez.Node()
camera = ez.Camera(parent=render)



camera.y = -3

target = ez.Node(parent=render)
#Create a camera for the buffer image:
buff_cam = ez.Camera(parent=target)
buff_cam.y = -5

#Create a texture buffer and assign the camera to it:
buffer = ez.TextureBuffer(256, 256)
buffer.camera = buff_cam

# Set the background color, will not show until the background is enabled:
buffer.background_color = (1,0,0,1)


#Load a flat plane and assign the buffer texture to its shader:
plane_mesh = ez.load.mesh('plane.bam')
plane = ez.Model(plane_mesh, parent=aspect2D)
plane.shader = ez.load.shader('base.glsl')
plane.set_shader_input('texture0', buffer.get_texture())
plane.scale = 0.2
plane.pos = -1, -0.7, 0
plane.transparency = True


#Lets load a model to look at:
hex_mesh = ez.load.mesh('hex.bam')
hex_model = ez.Model(hex_mesh, parent=render)
hex_model.shader = ez.load.shader('base.glsl')
dirt = ez.load.texture('dirt.png')
hex_model.set_shader_input('texture0', dirt)



def input(event):
    device, name, state = event

    # Toggle background on/off:
    if name=='q':
        if state==1:
            buffer.background = not buffer.background

    # Change background color:
    if name=='w' and state==1:
        if buffer.background:
            r, g, b, a = buffer.background_color
            if r == 1:
                r=0
                g=1
            elif g==1:
                g=0
                b=1
            else:
                b=0
                r=1
            buffer.background_color = r, g, b, a

    # Change background alpha:
    if name=='e' and state==1:
        if buffer.background:
            r, g, b, a = buffer.background_color
            if a==1.0:
                a = 0.5
            elif a==0.5:
                a = 0.0
            else:
                a = 1.0
            buffer.background_color = r, g, b, a

    if name == 'escape' and state == 0:
        ez.set_scene(ez['menu'])


def logic(dt):

    # Rotate the buffer's camera:
    if ez.is_button_down('r'):
        target.h += 100*dt
    hex_model.p += 20*dt


def enter():
    ez.window.background_color = 0, 0, 0

    ez.add_input_events(['q','w','e','r'])

    L, R, T, B = ez.window.get_aspect2D_edges()
    text = ez['text']
    text.x = L+0.02
    text.y = T-0.1
    text.text = "Q - Toggle background on/off"
    text.text += "\nW - Change background color"
    text.text += "\nE - Change background alpha"
    text.text += "\nR - Rotate buffer camera"
    text.parent = aspect2D


def exit():
    ez.remove_input_events(['q','w','e','r'])
