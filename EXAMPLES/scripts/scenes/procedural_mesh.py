render = ez.Node()
aspect2D = ez.Node()
camera = ez.Camera(parent=render)



camera.y = -10

pm = ez.ProceduralMesh()

#Lets make a flat plane:
verts = [
        #xyz vert   #normal direction
        0,  0, 0,   0, -1, 0,
        1,  0, 0,   0, -1, 0,
        1,  0, 1,   0, -1, 0,
        0,  0, 1,   0, -1, 0
]

# 0 is the first vert+normal, 1 is the second vert+normal, and so on:
tris = [
        #triangle
        0, 1, 2,
        0, 2, 3
]

pm.set_data(verts, tris)
mesh = pm.create_mesh()

model = ez.Model(mesh)
model.parent = render



def make_random_model():

    x1, y1, z1 = ez.random.point3D(-0.1, -1, 0, 0, -0.1, -1)
    x2, y2, z2 = ez.random.point3D(1, 0.1, 0, 0, -0.1, -1)
    x3, y3, z3 = ez.random.point3D(1, 0.1, 0, 0, 0.1, 1)
    x4, y4, z4 = ez.random.point3D(-1, -0.1, 0, 0, 0.1, 1)

    verts = [
            x1, y1, z1,  0, -1, 0,
            x2, y2, z2,  0, -1, 0,
            x3, y3, z3,  0, -1, 0,
            x4, y4, z4,  0, -1, 0
    ]

    tris = [
            0, 1, 2,
            0, 2, 3
    ]

    pm = ez.ProceduralMesh(verts=verts, tris=tris)
    mesh = pm.create_mesh()
    model = ez.Model(mesh)
    return model


ez['procedural_rmodel'] = None
def input(event):
    device, name, state = event

    if name=='q' and state==1:
        # Delete the old model so we won't leak memory:
        if ez['procedural_rmodel']:
            ez['procedural_rmodel'].parent = None

        rmodel = make_random_model()
        rmodel.x = -2
        rmodel.parent=render
        ez['procedural_rmodel'] = rmodel


    if name == 'escape' and state == 0:
        ez.set_scene(ez['menu'])


def logic(dt):
    pass


def enter():
    ez.window.background_color = 0, 0, 0
    ez.add_input_events(['q'])

    L, R, T, B = ez.window.get_aspect2D_edges()
    text = ez['text']
    text.x = L+0.02
    text.y = T-0.1
    text.parent=aspect2D
    text.text="Q - Draw randomized model"


def exit():
    ez.remove_input_events(['q'])

