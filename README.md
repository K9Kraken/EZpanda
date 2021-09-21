# EZpanda

EZpanda is a layer written for Panda3D to privide simplified game development.

A installed version of [Panda3D](https://github.com/panda3d/panda3d) is is required.

The "main.py" file initializes EZpanda as "ez" which is globaly available, "main.y" then loads and runs the 'menu' scene. Scenes are python modules, you can make your own scense and easily switch between them. Each scene has its own render, aspect2D, and camera.


Here is the template of a scene module:
```
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
```


Model loading and state changing example:

*NOTE: When finished with a EZnode like the model below you must call delete() on it to clear it from memory: model.delete(). The delete function will delete the node and any children it has.*
```
mesh = ez.load.mesh('ship.bam')
texture = ez.load.texture('ship.png')
shader = ez.load.shader('shaded.glsl')

model = ez.Model(mesh, parent=render)
model.shader = shader
model.set_shader_input('texture0', texture)

model.pos = 2, 0, 0
model.hpr = 100, 0, 0
model.z = 5
```


I focused EZpanda towards using your own shaders, however you can easily use Panda's shader system and access Panda's own nodes for example:
```
model.panda_node.set_pos(2, 0, 0)
```


Code examples are in the EXAMPLES folder, you can view them by running EXAMPLES/main.py.
Here is a list of the current examples:
```
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
```

