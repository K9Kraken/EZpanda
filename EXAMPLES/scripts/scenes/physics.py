render = ez.Node()
aspect2D = ez.Node()
camera = ez.Camera(parent=render)


# Setup constants for keyboard input:
MOUSE1, Q, W, E = keys = ['mouse1', 'q', 'w', 'e']
DOWN = 1
UP = 0


cam_target = ez.Node()
camera.pos = 0, -30, 30
camera.look_at(cam_target)


#Create the physics world:
world = ez.physics.World()


#for i in dir(physics.physics_world):
 #   print(i)

#Create an infinite plane that is facing up at position 0:
shape = ez.physics.shapes.Plane((0,0,1), 0)
plane = ez.physics.bodys.Rigid(shape)

#Tell phyisics what the plane will collide with:
ez.physics.set_mask(plane, ez.mask[1])


#Add the plane to the physics world:
world.add_body(plane)

#Just for parenting all the bodys to:
bodys = ez.Node(parent=render)

def make_body(mesh_name, image_name):

    #Lets give body a random scale, also effects mass:
    scale = ez.random.float()*2.0+0.2

    mesh = ez.load.mesh(mesh_name)
    model = ez.Model(mesh)

    model.scale = scale
    model.apply_transform()

    dirt = ez.load.texture(image_name)
    model.shader = ez.load.shader('shaded.glsl')
    model.set_shader_input('texture0', dirt)

    shape = ez.physics.shapes.make_convex_hull(model)
    #shape = ez.physics.shapes.make_triangle_mesh(hex_model)
    body = ez.physics.bodys.Rigid(shape, mass=scale*10.0)
    model.parent = body

    #Increase the friction to reduce sliding:
    body.friction = 1.0
    #Put some damping so body will not roll for so long:
    body.angular_damping = 0.25

    return body


def input(event):
    global count
    device, name, state = event

    if name is Q and state is DOWN:
        ball_body = make_body('sphere.bam', 'grass.png')
        ball_body.pos = ez.random.point3D(-3, 3, -3, 3, 15, 24)
        world.add_body(ball_body)
        ez.physics.set_mask(ball_body, ez.mask[1])
        ball_body.parent = bodys


    elif name is W and state is DOWN:
        hex_body = make_body('hex.bam', 'dirt.png')
        hex_body.pos = ez.random.point3D(-3, 3, -3, 3, 15, 24)
        hex_body.hpr = ez.random.hpr()
        world.add_body(hex_body)
        ez.physics.set_mask(hex_body, ez.mask[1])
        hex_body.parent = bodys

    elif name is E and state is DOWN:
        nodes = bodys.get_children()
        for node in nodes:
            node.delete()

    elif name is MOUSE1 and state is DOWN:
        fr, to = camera.get_projected_ray(ez.mouse.pos)
        hit = world.ray_test_closest(fr, to, mask=ez.mask[1])
        node = hit['NODE']

        if node is not plane:
            # If ray hits a body then wake it up and apply a velocity to it:
            node.active = True
            node.linear_velocity = 0, 0, 20




    if name=='escape' and state==0:
        ez.set_scene(ez['menu'])


def logic(dt):

    world.update(dt, 20, 1.0/360.0)




def enter():
    ez.window.background_color = 0, 0.0, 0.0
    ez.add_input_events(keys)

    L, R, T, B = ez.window.get_aspect2D_edges()
    text = ez['text']
    text.x = L+0.02
    text.y = T-0.1
    text.text = "Q - Drop ball"
    text.text += "\nW - Drop hexagon"
    text.text += "\nE - Delete all"
    text.text += "\nMOUSE - Click on body"
    text.parent = aspect2D



def exit():
    ez.remove_input_events(keys)
