render = ez.Node()
aspect2D = ez.Node()
camera = ez.Camera(parent=render)

camera.y=-200

mesh = ez.load.mesh('hex.bam')
shader = ez.load.shader('shaded.glsl')
dirt = ez.load.texture('dirt.png')

models = ez.SoftInstance(mesh, 1000, parent=render)
models.shader = shader
models.set_shader_input('texture0', dirt)

for model in models:
    model.pos = ez.random.point3D(-50, 50, -50, 50, -50, 50)
    model.hpr = ez.random.hpr()




def input(event):
    device, name, state = event

    if name == 'escape' and state == 0:
        ez.set_scene(ez['menu'])


def logic(dt):
    models.h+=3*dt
    for model in models:
        model.r+=ez.random.range(0,100)*dt
        model.p+=ez.random.range(0,100)*dt
        model.h+=ez.random.range(0,100)*dt




def enter():
    ez.window.background_color = 0, 0.0, 0.0


def exit():
    pass
