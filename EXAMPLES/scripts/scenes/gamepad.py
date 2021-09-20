render = ez.Node()
aspect2D = ez.Node()
camera = ez.Camera(parent=render)


def update_text():
    text = ez['text']
    text.text = ""

    if ez.gamepads:
        for gamepad in ez.gamepads:
            text.text += "\n"+gamepad.name+":    "+str(gamepad.device)
    else:
        text.text += "\nNo Gamepads detected"
    text.text += "\n"


buttons=[]
def input(event):
    device, name, state = event

    if "gamepad" in device:
        buttons.insert(0, device+":    "+name+"  "+str(state))
        update_text()
        if len(buttons) > 32:
            del buttons[-1]
        for button in buttons:
            ez['text'].text += "\n"+button



    if name=='escape' and state==0:
        ez.set_scene(ez['menu'])


def logic(dt):
    pass


def enter():
    ez.window.background_color = 0, 0.0, 0.0

    L, R, T, B = ez.window.get_aspect2D_edges()
    text = ez['text']
    ez['text'].scale = 0.04,  0.04,  0.04
    text.x = L+0.01
    text.y = T-0.01
    text.parent = aspect2D
    update_text()


def exit():
    ez['text'].scale = 0.06,  0.06,  0.06
