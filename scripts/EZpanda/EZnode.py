from panda3d.core import NodePath


# For copying and changing a nodes render states:
class RenderState:
    __slots__=(
        'name',
        'panda_node',
        'set_depth_write',
        'get_depth_write',
        'set_depth_offset',
        'get_depth_offset'
        )

    def __init__(self, EZnode, name):
        self.name = name
        state = EZnode.panda_node.get_state()
        self.panda_node = NodePath('')
        self.panda_node.set_state(state)

        # Need to add the other render states and setup properties.
        self.set_depth_write = self.panda_node.set_depth_write
        self.get_depth_write = self.panda_node.set_depth_write

        self.set_depth_offset = self.panda_node.set_depth_offset
        self.get_depth_offset = self.panda_node.get_depth_offset



# Primary EZ node
class Node():
    __slots__=(
        'name',
        '_parent',
        '_shader',
        '_colliders',
        'panda_node',
        'show',
        'hide',
        'is_hidden',
        'set_billboard_axis',
        'set_billboard_point_world',
        'set_billboard_point_eye',
        'clear_billboard',
        'do_billboard_axis',
        'do_billboard_point_world',
        'do_billboard_point_eye'
        )

    def __init__(self, panda_node=None, parent=None):
        self.name = 'EZnode'

        self._parent = None
        self._shader = None
        # Used by delete() to remove self from any collision handlers:
        self._colliders = []

        if panda_node:
            if panda_node.has_tag('copy'):
                # Here we copy the panda node so we don't have to keep loading it:
                panda_node = NodePath( panda_node.node().copy_subgraph() )
            self.panda_node = panda_node
        else:
            self.panda_node = NodePath('EZnode')

        # Reference to self on panda_nod, prevents garbage collection so must call self.delete()
        self.panda_node.set_python_tag('EZnode', self)
        # Used for locating panda_node:
        self.panda_node.set_tag('panda_node', '')

        # Pass in functions:
        self.hide = self.panda_node.hide
        self.show = self.panda_node.show
        self.is_hidden = self.panda_node.is_hidden
        self.set_billboard_axis = self.panda_node.set_billboard_axis
        self.set_billboard_point_world = self.panda_node.set_billboard_point_world
        self.set_billboard_point_eye = self.panda_node.set_billboard_point_eye
        self.clear_billboard = self.panda_node.clear_billboard
        self.do_billboard_axis = self.panda_node.do_billboard_axis
        self.do_billboard_point_eye = self.panda_node.do_billboard_point_eye
        self.do_billboard_point_world = self.panda_node.do_billboard_point_world

        # Remove all collision masks:
        self.panda_node.set_collide_mask(0)

        # Set the parent:
        self.parent = parent


    def delete(self):
        # Remove node from any collision colliders:
        for collider in self._colliders:
            collider.remove_collider(self)

        for child in self.panda_node.get_children():
            EZnode = child.get_python_tag('EZnode')
            if EZnode:
                EZnode.delete()

        self.parent = None
        self.panda_node.clear_python_tag('EZnode')
        self.panda_node.remove_node()

    def get_children(self):
        children = []
        for child in self.panda_node.get_children():
            EZnode = child.get_python_tag('EZnode')
            if EZnode:
                children.append(EZnode)
        return children

    def look_at(self, node_or_pos):
        if isinstance(node_or_pos, ez.Node):
            self.panda_node.look_at(node_or_pos.panda_node)
        else:
            self.panda_node.look_at(node_or_pos)

    def get_distance_to(self, node ):
        return self.panda_node.get_distance( node.panda_node )

    def get_facing_vector(self):
        return self.parent.panda_node.get_relative_vector(self.panda_node, (0,1,0))

    def get_relative_vector(self, node, vec3):
        return self.panda_node.get_relative_vector(node.panda_node, vec3)

    def apply_transform(self):
        # state = self.panda_node.get_state() #Get the render state so we can restore it after flattening: (may not be needed)
        self.panda_node.flatten_light()
        # self.panda_node.set_state(state)

        # set_shader_input('a', 1)
    def set_shader_input(self, shader_value_name, value):
        if isinstance(value, ez.Node):
            value = value.panda_node
        self.panda_node.set_shader_input(shader_value_name, value)

        # set_shader_inputs(a=1, b=2, ..) or set_shader_inputs(**dict):
    def set_shader_inputs(self, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, ez.Node):
                print(kwargs[key])
                kwargs[key] = value.panda_node
                print(kwargs[key])
        self.panda_node.set_shader_inputs(**kwargs)

    @property
    def parent(self):
        return self._parent
    @parent.setter
    def parent(self, EZnode):
        if EZnode:
            self.panda_node.reparent_to(EZnode.panda_node)
            self._parent = EZnode

        else:
            self.panda_node.detach_node()
            self._parent = None

    # Get relative from node:
    def get_rx(self, node ):
        return self.panda_node.get_x(node.panda_node)
    def get_ry(self, node ):
        return self.panda_node.get_y(node.panda_node)
    def get_rz(self, node ):
        return self.panda_node.get_z(node.panda_node)
    def get_rpos(self, node):
        return self.panda_node.get_pos(node.panda_node)
    def get_rh(self, node):
        return self.panda_node.get_h(node.panda_node)
    def get_rp(self, node):
        return self.panda_node.get_p(node.panda_node)
    def get_rr(self, node):
        return self.panda_node.get_r(node.panda_node)
    def get_rhpr(self, node):
        return self.panda_node.get_hpr(node.panda_node)

    # Set relative to node:
    def set_rx(self, x, node):
        self.panda_node.set_x(node.panda_node, x)
    def set_ry(self, y, node):
        self.panda_node.set_y(node.panda_node, y)
    def set_rz(self, z, node):
        self.panda_node.set_z(node.panda_node, z)
    def set_rpos(self, pos, node):
        self.panda_node.set_pos(node.panda_node, pos)
    def set_rh(self, h, node):
        self.panda_node.set_h(node.panda_node, h)
    def set_rp(self, p, node):
        self.panda_node.set_p(node.panda_node, p)
    def set_rr(self, r, node):
        self.panda_node.set_r(node.panda_node, r)
    def set_rhpr(self, hpr, node):
        self.panda_node.set_hpr(node.panda_node, hpr)

    # Relative to parent:
    @property
    def x(self):
        return self.panda_node.get_x()
    @x.setter
    def x(self, value):
        self.panda_node.set_x(value)

    @property
    def y(self):
        return self.panda_node.get_y()
    @y.setter
    def y(self, value):
        self.panda_node.set_y(value)

    @property
    def z(self):
        return self.panda_node.get_z()
    @z.setter
    def z(self, value):
        self.panda_node.set_z(value)

    @property
    def pos(self):
        return self.panda_node.get_pos()
    @pos.setter
    def pos(self, value):
        self.panda_node.set_pos(value)

    @property
    def h(self):
        return self.panda_node.get_h()
    @h.setter
    def h(self, value):
        self.panda_node.set_h(value)

    @property
    def p(self):
        return self.panda_node.get_p()
    @p.setter
    def p(self, value):
        self.panda_node.set_p(value)

    @property
    def r(self):
        return self.panda_node.get_r()
    @r.setter
    def r(self, value):
        self.panda_node.set_r(value)

    @property
    def hpr(self):
        return self.panda_node.get_hpr()
    @hpr.setter
    def hpr(self, value):
        self.panda_node.set_hpr(value)

    @property
    def scale(self):
        return self.panda_node.get_scale()
    @scale.setter
    def scale(self, value):
        self.panda_node.set_scale(value)

    # Render settings:
    def copy_render_state(self, custom_name):
        return RenderState(self, custom_name)

    def set_render_state(self, state):
        self.panda_node.set_state(state.panda_node.get_state())

    def set_render_state_to_camera(self, state, camera):
        camera.add_render_state(state, state.name)
        self.panda_node.set_tag(camera.panda_node.node().tag_state_key, state.name)

    @property
    def shader(self):
        return self.panda_node.get_shader()
    @shader.setter
    def shader(self, shader):
        self.panda_node.set_shader(shader)
        self._shader = shader

    @property
    def depth_write(self):
        return self.panda_node.get_depth_write()
    @depth_write.setter
    def depth_write(self, bool_):
        self.panda_node.set_depth_write(bool_)

    @property
    def transparency(self):
        return self.panda_node.get_transparency()
    @transparency.setter
    def transparency(self, transparency_flag):
        self.panda_node.set_transparency(transparency_flag)