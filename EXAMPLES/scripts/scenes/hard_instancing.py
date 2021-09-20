render = ez.Node()
aspect2D = ez.Node()
camera = ez.Camera(parent=render)


total_instances = 300000
bounds = (600, 20000, 500)

mesh = ez.load.mesh('hex.bam')
shader = ez.load.shader('hard_instance_shaded.glsl')
dirt = ez.load.texture('dirt.png')

models = ez.HardInstance(mesh, total_instances, bounds, hpr=(0, 90, 0), parent=render)
models.generate_random_pos(scale_min=0.2, scale_max=2.0)

models.shader = shader
models.set_shader_input('texture0', dirt)


camera.y = -11000

def input(event):
    device, name, state = event

    if name == 'escape' and state == 0:
        ez.set_scene(ez['menu'])


def logic(dt):
    if ez.is_button_down('q'):
        models.h += 20*dt
    if ez.is_button_down('w'):
        models.h -= 20*dt
    if ez.is_button_down('e'):
        camera.y = -11000
        models.h = 0

    camera.y += 200*dt
    if camera.y > 10000:
        camera.y = -11000


def enter():
    ez.window.background_color = 0, 0.0, 0.0


def exit():
    pass
