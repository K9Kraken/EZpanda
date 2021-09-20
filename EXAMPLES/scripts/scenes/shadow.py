render = ez.Node()
aspect2D = ez.Node()
camera = ez.Camera(parent=render)


sun = ez.lights.Sun(parent=render)
sun.pos = -20, 0 ,20
sun.look_at(render)

# Lets show the bounds of the light:
sun.show_frustum()


shader = ez.load.shader('shadow.glsl')

pmesh = ez.load.mesh('plane2.bam')
plane = ez.Model(pmesh, parent=render)
plane.shader = shader
plane.set_shader_input('sun', sun)


smesh = ez.load.mesh('sphere.bam')
sphere = ez.Model(smesh, parent=render)
sphere.z = 2


camera.pos = 0, -20, 20
camera.look_at( plane )


def input(event):
    device, name, state = event

    if name == 'escape' and state == 0:
        ez.set_scene( ez['menu'] )



direction = ez.Vec3(0,0,1)
def logic(dt):
    sphere.pos += direction*4*dt
    if sphere.z > 8 or sphere.z < -1:
        direction.z *= -1


def enter():
    pass

def exit():
    pass
