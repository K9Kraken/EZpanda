render = ez.Node()
aspect2D = ez.Node()
camera = ez.Camera(parent=render)

camera.y = -10

line = ez.Line(parent=render)
line.set_thickness(1)

line.set_color(0, 0, 1, 1)
line.move_to(0, 0, 0)

line.set_color(1, 0, 0, 1)
line.draw_to(1, 0, 0)

line.set_color(0, 1, 0, 1)
line.draw_to(1, 0, 1)

line.set_color(0, 0, 1, 1)
line.draw_to(0, 0, 0)

line.create()



def input(event):
    device, name, state = event

    if name == 'escape' and state == 0:
        ez.set_scene(ez['menu'])


def logic(dt):
    line.h+=100*dt
    pass


def enter():
    ez.window.background_color = 0, 0, 0


def exit():
    pass
