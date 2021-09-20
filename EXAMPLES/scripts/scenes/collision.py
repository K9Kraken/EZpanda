render = ez.Node()
aspect2D = ez.Node()
camera = ez.Camera(parent=render)

camera.y = -20


# Create collision shapes:

# Collision Sphere:
sphere = ez.collision.shapes.Sphere(0.25, parent=render)
sphere.parent = None
sphere.parent = render
# Collide from mask 2:
ez.collision.set_mask(sphere, ez.mask[2])
# Set what sphere will collide to:
ez.collision.set_target_mask(sphere, ez.mask[1])
sphere.pos = 0, 0 , 0
# Show the shape so we can see what it is doing, for dubugging:
sphere.show()
sphere.name = "Sphere"

# Collision Capsule:
capsule = ez.collision.shapes.Capsule((0,0,0), (0,0,1), 0.25, parent=render)
ez.collision.set_mask(capsule, ez.mask[1])
capsule.pos = -4, 0, 0
capsule.show()
capsule.name = "Capsule"

# Collision Box:
box = ez.collision.shapes.Box((0.5, 0.25, 1), origin=(0, 0, 0.5), parent=render)
ez.collision.set_mask(box, ez.mask[1])
box.pos = 4, 0, 0
box.show()
box.name = "Box"


# Rays, they are only used for hitting other objects:

pos = -2, 0 , -1
to_pos = 0, 0, 2
segment = ez.collision.rays.Segment( pos, to_pos, parent=render)
ez.collision.set_target_mask(segment, ez.mask[2])
segment.show()
segment.name = "Segment"

from_pos = 1, 0, 1
towards = 0, 0, -1
ray = ez.collision.rays.Ray( from_pos, towards, parent=render )
ez.collision.set_target_mask(ray, ez.mask[2])
ray.show()
ray.name = "Ray"

pos = 2, 0, 0
direction = 0, 0, 1
line = ez.collision.rays.Line( pos, direction, parent=render)
ez.collision.set_target_mask(line, ez.mask[2])
line.show()
line.name = "line"



# Create a collision handler and add colliders:
handler = ez.collision.Handler()
handler.add_collider(sphere)

handler.add_collider(segment)
handler.add_collider(ray)
handler.add_collider(line)



def input(event):
    device, name, state = event

    if name == 'escape' and state == 0:
        ez.set_scene(ez['menu'])


def logic(dt):
    hits = handler.get_collisions(render)
    if hits:
        for hit in hits:
            from_name = hit['FROM'].name
            into_name = hit['INTO'].name
        text = ez['text']
        text.text = "W - move left"
        text.text += "\nD - move right\n"
        text.text += from_name+" HIT "+into_name+" AT "+str(hit['POS'])

    if ez.is_button_down('a'):
        if sphere.x > -5:
            sphere.x -= 2*dt
    if ez.is_button_down('d'):
        if sphere.x < 5:
            sphere.x += 2*dt


def enter():
    ez.window.background_color = 0, 0, 0

    L, R, T, B = ez.window.get_aspect2D_edges()
    text = ez['text']
    text.text = "W - move left"
    text.text += "\nD - move right"
    text.x = L+0.01
    text.y = T-0.08
    text.parent = aspect2D




def exit():
    pass
