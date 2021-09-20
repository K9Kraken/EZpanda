render = ez.Node()
aspect2D = ez.Node()
camera = ez.Camera(parent=render)

camera.y = -20

# Create a a model:
dirt = ez.load.texture('dirt.png')
mesh = ez.load.mesh('hex.bam')
model = ez.Model( mesh, parent=render)
model.shader = ez.load.shader('shaded.glsl')
model.set_shader_input('texture0', dirt)

# Our task function:
def task_spin_node(node, task):
    node.p += 100 * ez.get_dt()
    return task.cont

# Create the task and pass model as the node:
task = ez.make_task(task_spin_node, model)

# You can pass whatever you want into a task: (task will always be last argument)
# Example:
#def task_fuction(a, b, c, d, e, LIST, DICT, task):
#    return task.cont
# task = ez.make_task(task_function, a, b, d, c, e, LIST, DICT)



def input(event):
    device, name, state = event

    if name=='space':
        if state==1:
            ez.add_task(task)
        else:
            ez.remove_task(task)

    if name == 'escape' and state == 0:
        ez.set_scene(ez['menu'])


def logic(dt):
    if ez.is_button_down('a'):
        pos[0] -= 10*dt
        if pos[0] < 1:
            pos[0] = 1
    if ez.is_button_down('d'):
        pos[0] += 10*dt
        if pos[0] > 6:
            pos[0] = 6



def enter():
    ez.window.background_color = 0, 0.0, 0.0
    ez.add_input_events(['space'])
    L, R, T, B = ez.window.get_aspect2D_edges()
    text = ez['text']
    text.x = L+0.02
    text.y = B+0.03
    text.text="SPACE - down: adds the task, release: removes the task"
    text.parent = aspect2D


def exit():
    ez.remove_input_events(['space'])

    # If holding down the space bar and exiting the task can keep running in the background.
    # So here we are removing the task to make sure it stops running when leaving the scene.
    ez.remove_task(task)
