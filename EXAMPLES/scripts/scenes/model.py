render = ez.Node()
aspect2D = ez.Node()
camera = ez.Camera(parent=render)

# Lets move the camera back so we can see objects at 0, 0, 0
camera.y = -10


# Load the mesh from file, (This is a normal panda model load):
mesh = ez.load.mesh('hex.bam')
# Load a image:
dirt = ez.load.texture('dirt.png')
# Load a shader:
shader = ez.load.shader('shaded.glsl')



# Create a model:
model = ez.Model(mesh, parent=render)
model.shader = shader
model.set_shader_input('texture0', dirt)

# Change model position:
model.pos = 2, 0, 0
# Change model rotation:
model.hpr = 100, 0, 0

# Other state change examples:
# model.x = 2
# model.y = 0
# model.z = 0
# modep.h = 100
# modep.p = 0
# modep.r = 0

#You can change relative to another node:
#mode.set_rpos(node, pos)
#mode.set_rx(node, pos)


# You can create a node and apply the shader and images to it.
# Anything parented to this node will inharent the shader:
node = ez.Node(parent=render)
node.shader = shader
node.set_shader_input('texture0', dirt)


# Now just create models and parent them to node:
for i in range(0,5):
    m = ez.Model(mesh, parent=node)
    m.x = -2
    m.z = i-2


# NOTE
# When finished with a node you must call node.delete() as it is not garbage collected.
# (node.delete() will remove the node and all its children)


def input(event):
    device, name, state = event

    if name=='escape' and state==0:
        ez.set_scene( ez['menu'] )


def logic(dt):
    #Lets rotate the model in realtime:
    model.p += 50*dt

def enter():
    ez.window.background_color = 0, 0.0, 0.0


def exit():
    pass

