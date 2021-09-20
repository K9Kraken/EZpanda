render = ez.Node()
aspect2D = ez.Node()
camera = ez.Camera(parent=render)


mesh = ez.load.mesh('plane.bam')
mhex = ez.Model(mesh, parent=aspect2D)
mhex.scale = 0.2

def set_ui_pos():
    padding = 0.22
    L, R, T, B = ez.window.get_aspect2D_edges()

    mhex.x = L + padding
    mhex.y = T - padding

    text = ez['text']
    text.x = L+0.02
    text.y = B+0.03

set_ui_pos()

default_width, default_height = ez.window.get_size()

refresh_rate = ez.window.get_display_mode(0)[2]

def input(event):
    device, name, state = event

    w, h = ez.window.get_size()
    if name=='space' and state==0:
        if w==default_width:
            w = 1200
            h = 600
        elif w==1200:
            w = 300
            h = 1024
        elif w==600:
            w = 800
            h = 600
        elif w==800:
            w = 960
            h = 320
        else:
            w = default_width
            h = default_height

        ez.window.set_display(w, h, refresh_rate)

        set_ui_pos()
        #After changing resolution might be good idea to set the 3D camera apsect to it to prevent 3D stretching:
        camera.set_aspect_ratio(ez.window.get_aspect_ratio())

    if name == 'escape' and state == 0:
        ez.set_scene(ez['menu'])


def logic(dt):
    ez.add_input_events(['space'])


def enter():
    ez.window.background_color = 0, 0.0, 0.0
    L, R, T, B = ez.window.get_aspect2D_edges()
    text = ez['text']
    text.x = L+0.02
    text.y = B+0.03
    text.text="SPACE - Change Resolution"
    text.parent = aspect2D


def exit():
    ez.remove_input_events(['space'])
    ez.window.set_display(default_width, default_height, refresh_rate)

    # Just setting UI to default resolution so they will be placed right when coming back in:
    set_ui_pos()
