render = ez.Node()
aspect2D = ez.Node()
camera = ez.Camera(parent=render)



ez.add_input_events(['escape'])
ez['world'] = ez.load.scene('world')



def input(event):
    device, name, state = event

    if name == 'space' and state == 0:
        ez.set_scene( ez['world'] )

    if name == 'escape' and state == 0:
        ez.end()


def logic(dt):
    pass


def enter():
    print("MENU")
    ez.add_input_events(['space'])




def exit():
    ez.remove_input_events(['space'])
