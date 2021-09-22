render = ez.Node()
aspect2D = ez.Node()
camera = ez.Camera(parent=render)


# Setup constants for keyboard input:
MOUSE1, Q, W, E, R = keys = ['mouse1', 'q', 'w', 'e', 'r']
DOWN = 1
UP = 0

MASK_COLLISION = ez.mask[1]
MASK_MOUSE_RAY = ez.mask[2]
MASK_MOUSE_RAY2 = ez.mask[3]

cam_target = ez.Node()
camera.pos = 0, -30, 30
camera.look_at(cam_target)


# Create the physics world:
world = ez.physics.World()


# Create an infinite plane that is facing up at position 0:
shape = ez.physics.shapes.Plane((0,0,1), 0)
plane = ez.physics.bodys.Rigid(shape)

# Tell phyisics what the plane will collide with:
ez.physics.set_mask(plane, MASK_COLLISION)


# Add the plane to the physics world:
world.add_body(plane)

# Just for parenting all the bodys to:
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

# Just using to keep tack of toggling mouse clicking for hexagons:
mouse_hex_pick = [False]
def input(event):
    global count
    device, name, state = event

    if name is Q and state is DOWN:
        ball_body = make_body('sphere.bam', 'grass.png')
        ball_body.pos = ez.random.point3D(-3, 3, -3, 3, 15, 24)
        world.add_body(ball_body)
        # Same mask as the plane so they will collide:
        ez.physics.set_mask(ball_body, MASK_COLLISION)
        # Add mask[2] which is what the ray from the mouse uses:
        ez.physics.add_mask(ball_body, MASK_MOUSE_RAY)
        # You can also do this:
        # masks = MASK_COLLISION | MASK_MOUSE_RAY       # Bitwise add masks together.
        # ez.physics.set_mask(ball_body, masks)
        ball_body.parent = bodys
        ball_body.name = "sphere"


    elif name is W and state is DOWN:
        hex_body = make_body('hex.bam', 'dirt.png')
        hex_body.pos = ez.random.point3D(-3, 3, -3, 3, 15, 24)
        hex_body.hpr = ez.random.hpr()
        world.add_body(hex_body)
        # Same mask as the plane and the spheres so they will all collide together:
        ez.physics.set_mask(hex_body, MASK_COLLISION)
        # Adding mask used for toggling mouse picking on hex models:
        ez.physics.add_mask(hex_body, MASK_MOUSE_RAY2)

        hex_body.parent = bodys
        hex_body.name = "hex"

    # Toggle mouse clicking ON/OFF for spheres:
    elif name is E:
        if state is DOWN:
            mouse_hex_pick[0] = True
        else:
            mouse_hex_pick[0] = False


    elif name is R and state is DOWN:
        nodes = bodys.get_children()
        for node in nodes:
            node.delete()

    elif name is MOUSE1 and state is DOWN:
        fr, to = camera.get_projected_ray(ez.mouse.pos)
        if mouse_hex_pick[0]:
            hit = world.ray_test_closest(fr, to, mask=MASK_MOUSE_RAY | MASK_MOUSE_RAY2)
        else:
            hit = world.ray_test_closest(fr, to, mask=MASK_MOUSE_RAY)
        if hit:
            node = hit['NODE']
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
    text.text += "\nE - Hold to enable mouse picking for hexagons"
    text.text += "\nR - Delete all"
    text.text += "\nMOUSE - Click over body"
    text.parent = aspect2D



def exit():
    ez.remove_input_events(keys)
