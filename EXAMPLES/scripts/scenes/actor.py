render = ez.Node()
aspect2D = ez.Node()
camera = ez.Camera(parent=render)




mesh = ez.load.mesh('wiggle.bam')
shader = ez.load.shader('actor_shaded.glsl')
texture = ez.load.texture('dirt.png')


actor = ez.Actor(mesh, parent=render)
actor.shader = shader
actor.set_shader_input('texture0', texture)

actor.loop('walk')


camera.pos = 0, -5, 5
camera.look_at(actor)



def input(event):
    device, name, state = event

    if name == 'escape' and state == 0:
        ez.set_scene(ez['menu'])


def logic(dt):
    actor.h += 100*dt


def enter():
    ez.window.background_color = 0, 0.0, 0.0


def exit():
    pass
