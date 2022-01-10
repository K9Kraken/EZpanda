render = ez.Node()
aspect2D = ez.Node()
camera = ez.Camera(parent=render)


camera.y = -10

#Create a mouse picker for the camera:
mouse_picker = ez.collision.MousePicker(camera, mask=ez.mask[1])

#Create a mouse picker for aspect2D:
mouse_picker2D = ez.collision.MousePickre2D(mask=ez.mask[1])

#Load a 2D plane and parent it to aspect2D:
mesh = ez.load.mesh('plane.bam')
plane = ez.Model(mesh, parent=aspect2D)
plane.scale = 0.2
plane.x = -0.2
plane.name = "Aspect2D_Plane"
ez.collision.set_mask(plane, ez.mask[1])


#Create a model to click on:
dirt = ez.load.texture('dirt.png')
hex_land = ez.Model( ez.load.mesh('hex.bam'), parent=render)
hex_land.shader = ez.load.shader('base.glsl')
hex_land.set_shader_input('texture0', dirt)
hex_land.p = 45
hex_land.name = "Hex_Model"


# Collision Capsule:
capsule = ez.collision.shapes.Capsule((0,0,0), (0,0,1), 0.25, parent=render)
ez.collision.set_mask(capsule, ez.mask[1])
capsule.pos = 0, -1, 0
capsule.show()
capsule.name = "Collision_Capsule"

#Enable the same mask on the picker on the hex_land:
ez.collision.set_mask(hex_land, ez.mask[1])



# Lets make a font and turn it in to a clickable node:
font = ez.load.font('OpenSans-Regular.ttf')
t = ez.Text(font)
t.text = "Hello World!"
t.align = t.A_CENTER
t.scale = 0.1
t.color = 1.0, 0.5, 0.0, 1.0

t.set_frame_margin( (0, 0, 0, 0) )
t.frame_color = 0.0, 0.5, 0.5, 1.0

t.set_card_margin( (0, 0, 0, 0) )
t.card_color = 0.4, 0.1, 0.1, 1

t.frame_width = 3
t.frame_corners = True


tmesh = t.make_mesh()

tnode = ez.Node(tmesh)
tnode.name = "Hello World"
tnode.parent = aspect2D
tnode.pos = 0.5, 0.5, 0

# Make the generate next node clickable: (It is not perfect, gerated card does not cover text perfectly, need to look in to this)
ez.collision.set_mask(tnode, ez.mask[1])


def input(event):
    device, name, state = event

    if name == 'mouse1' and state == 1:
        text = ez['text']
        #See if the mouse hits anything in UI:
        hit = mouse_picker2D.get_hit(aspect2D)
        if hit:
            text.text="Mouse Selected UI: "+hit['NODE'].name
            text.text+="\nPosition: "+str(hit['POS'])
            hit['NODE'].h += 6.0
        else:
            #See if the mouse hits anying on the render node:
            hit = mouse_picker.get_hit(render)
            if hit:
                text.text="Mouse Selected: "+hit['NODE'].name
                text.text+="\nSelected Normal: "+str(hit['NORMAL'])
                text.text+="\nPosition: "+str(hit['POS'])
                node = hit['NODE']
                node.set_rr(-6.0, node)
            else:
                text.text="Nothing selected"
                text.text+="\nPosition: "+str(ez.mouse.pos)

    if name == 'escape' and state == 0:
        ez.set_scene(ez['menu'])


def logic(dt):
    pass


def enter():
    ez.window.background_color = 0, 0.0, 0.0

    ez.add_input_events(['mouse1'])
    #Change the mouse cursor:
    ez.mouse.cursor = ez.load.cursor('m.cur')

    text = ez['text']
    L, R, T, B = ez.window.get_aspect2D_edges()
    text.x = L+0.02
    text.y = T-0.1
    text.text = ""
    text.parent = aspect2D



def exit():
    ez.remove_input_events(['mouse1'])
    #Clear the custom mouse cursor:
    ez.mouse.cursor = None
