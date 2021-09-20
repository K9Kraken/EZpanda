render = ez.Node()
aspect2D = ez.Node()
camera = ez.Camera(parent=render)


#Create particles using "point_fountain" config file:
#(render_parent is the node space where the individual particles are rendered to)
part = ez.particles.Particle('point_fountain', parent=render, render_parent=render)


#Move particle generator in front of camera:
part.y = 10


def input(event):
    device, name, state = event

    if name=='q' and state==1:
        part.disable()

    elif name=='w' and state==1:
        part.enable()

    elif name=='e' and state==1:
        #Turn particles off:
        part.off()
    elif name=='r' and state==1:
        #Turn particles on with a delay of 1 second:
        #part.on(1)
        part.on()

    if name=='escape' and state==0:
        ez.set_scene(ez['menu'])



def logic(dt):
    pass


def enter():
    ez.window.background_color = 0, 0.0, 0.0
    ez.add_input_events(['q', 'w', 'e', 'r' ])

    text = ez['text']
    L, R, T, B = ez.window.get_aspect2D_edges()
    text.x = L+0.02
    text.y = T-0.1
    text.text = "Q - disable particle"
    text.text += "\nW - enable particle"
    text.text += "\nE - turn off particles"
    text.text += "\nR - turn on particles"
    text.parent = aspect2D

    part.enable()


def exit():
    ez.remove_input_events(['q', 'w', 'e', 'r' ])


    part.disable()
