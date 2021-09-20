render = ez.Node()
aspect2D = ez.Node()
camera = ez.Camera(parent=render)



def input(event):
    device, name, state = event

    if name == 'escape' and state == 0:
        ez.end()


def logic(dt):
    pass


def enter():
    pass


def exit():
    pass
