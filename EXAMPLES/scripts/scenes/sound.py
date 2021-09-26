render = ez.Node()
aspect2D = ez.Node()
camera = ez.Camera(parent=render)


# Music:
music = ez.load.music('Asking Questions.ogg')

# Sound:
sound = ez.load.sound('sweep.wav')

# Multiple sounds, doesn't use more memory as they all point to the same wav file:
sounds = []
for i in range(0,10):
    sound = ez.load.sound('sweep.wav')
    sounds.append(sound)


# 3D sound attached to a node:
mesh = ez.load.mesh('sphere.bam')
sphere = ez.Model(mesh, parent=render)
sphere.y = 200

ez.audio3D.listener = camera
sound3D = ez.load.sound3D('zap.wav')
sound3D.node = sphere


def input(event):
    device, name, state = event

    if name=='q' and state==1:
        if music.get_status() is ez.flags.sound.READY:
            music.play()
        elif music.get_status() is ez.flags.sound.PLAYING:
            music.stop()

    if name=='w' and state==1:
        sound3D.loop = not sound3D.loop
        sound3D.play()

    if name=='e' and state==1:
        sound.rate=ez.random.float()*2.0+0.2
        sound.play()

    if name=='r' and state==1:
        for s in sounds:
            if s.get_status() is ez.flags.sound.READY:
                s.rate=ez.random.float()*2.0+0.2
                s.play()
                break

    if name == 'escape' and state == 0:
        ez.set_scene(ez['menu'])


direction = ez.Vec3(0,1,0)
def logic(dt):

    sphere.pos += direction*50*dt
    if sphere.y > 200 or sphere.y < 2:
        direction.y *= -1



def enter():
    ez.window.background_color = 0, 0, 0
    ez.add_input_events(['q','w','e','r'])

    L, R, T, B = ez.window.get_aspect2D_edges()
    text = ez['text']
    text.x = L+0.02
    text.y = T-0.1
    text.text="Q - Toggle music"
    text.text+="\nW - Toggle 3D sound on sphere"
    text.text+="\nE - Play sound (Only can play 1 at a time)"
    text.text+="\nR -  Play sound (Play multple at same time)"
    text.parent=aspect2D


def exit():
    #music.stop()
    sound3D.stop()
    sound3D.loop=False
    ez.remove_input_events(['q','w','e','r'])
