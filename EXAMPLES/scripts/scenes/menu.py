render = ez.Node()
aspect2D = ez.Node()
camera = ez.Camera(parent=render)

ez.window.show_fps = True


# Lets create a global text object that all the scenes can use:
font = ez.load.font('OpenSans-Regular.ttf')
ez['text'] = ez.Text(font)
ez['text'].scale = 0.06,  0.06,  0.06


def input(event):
    device, name, state = event
    # Move mouse to center of window:
    ez.mouse.pos = 0, 0

    if name=='a' and state==0:
        scene = ez.load.scene('sound')
        ez.set_scene(scene)
    if name=='b' and state==0:
        scene = ez.load.scene('model')
        ez.set_scene(scene)
    elif name=='c' and state==0:
        scene = ez.load.scene('actor')
        ez.set_scene(scene)
    elif name=='d' and state==0:
        scene = ez.load.scene('soft_instancing')
        ez.set_scene(scene)
    elif name=='e' and state==0:
        scene = ez.load.scene('hard_instancing')
        ez.set_scene(scene)
    elif name=='f' and state==0:
        scene = ez.load.scene('collision')
        ez.set_scene(scene)
    elif name=='g' and state==0:
        scene = ez.load.scene('physics')
        ez.set_scene(scene)
    elif name=='h' and state==0:
        scene = ez.load.scene('placing_UI')
        ez.set_scene(scene)
    elif name=='i' and state==0:
        scene = ez.load.scene('procedural_mesh')
        ez.set_scene(scene)
    elif name=='j' and state==0:
        scene = ez.load.scene('render2texture')
        ez.set_scene(scene)
    elif name=='k' and state==0:
        scene = ez.load.scene('mouse')
        ez.set_scene(scene)
    elif name=='l' and state==0:
        scene = ez.load.scene('tasks')
        ez.set_scene(scene)
    elif name=='m' and state==0:
        scene = ez.load.scene('draw_line')
        ez.set_scene(scene)
    elif name=='n' and state==0:
        scene = ez.load.scene('gamepad')
        ez.set_scene(scene)
    elif name=='o' and state==0:
        scene = ez.load.scene('particles')
        ez.set_scene(scene)
    elif name=='p' and state==0:
        scene = ez.load.scene('shadow')
        ez.set_scene(scene)
    elif name=='q' and state==0:
        scene = ez.load.scene('depth')
        ez.set_scene(scene)


    if name=='escape' and state==0:
        ez.end()



def logic(dt):
    pass


keys=['a','b', 'c','d','e','f','g','h','i','j','k','l','m','n','o','p','q']
def enter():

    ez.add_input_events(['escape']+keys)
    ez.window.background_color = 0.41, 0.41, 0.41

    # Set menu text:
    text = ez['text']
    text.y=0.85
    text.x=-0.5
    text.align = text.A_LEFT
    choices="""
        A - Sound
        B - Model
        C - Actor
        D - Soft Instancing
        E - Hard Instancing
        F - Collision
        G - Physics
        H - Placing UI
        I - Procedural Mesh
        J - Render to Texture
        K - Mouse
        L - Tasks
        M - Draw Line
        N - Gamepad
        O - Particles
        P - Shadow
        Q - Depth Map
        """
    text.text = choices
    text.parent = aspect2D



def exit():
    ez.remove_input_events(keys)