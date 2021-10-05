render = ez.Node()
aspect2D = ez.Node()
camera = ez.Camera(parent=render)

camera.pos = (0, -30, 25)


mesh = ez.load.mesh('plane2.bam')
shader = ez.load.shader('depth.glsl')

plane = ez.Model(mesh, parent=render)
plane.shader = shader

plane.depth_write = False
plane.transparency = ez.flags.transparency.ALPHA


depth = camera.create_depth_map()
res = depth.get_x_size(), depth.get_y_size()

plane.set_shader_inputs(depth_map=depth, depth_resolution=res, near=1, far=1000)

camera.look_at(plane)

# Hexagon:
mesh = ez.load.mesh('hex.bam')
shader = ez.load.shader('shaded.glsl')
texture = ez.load.texture('grass.png')

hexagon = ez.Model(mesh, parent=render)
hexagon.scale = 2.0
hexagon.p = 90
hexagon.shader = shader
hexagon.set_shader_inputs(texture0=texture)

start = (2, 0, 8)
stop = (2, 0, -8)
rate = 10
itv = ez.intervals.pos(hexagon, start, stop, rate)


# Sphere:
mesh = ez.load.mesh('sphere.bam')
shader = ez.load.shader('shaded.glsl')
texture = ez.load.texture('dirt.png')

sphere = ez.Model(mesh, parent=render)
sphere.scale = 2.0
sphere.shader = shader
sphere.set_shader_inputs(texture0=texture)

itv2 = ez.intervals.pos(sphere, (-2, 0, -8), (-2, 0, 8), 8)




def input(event):
    device, name, state = event

    if name == 'escape' and state == 0:
        ez.set_scene(ez['menu'])


def logic(dt):
    hexagon.h += 50*dt


def enter():
    itv.loop()
    itv2.loop()

def exit():
    itv.finish()
    itv2.finish()
