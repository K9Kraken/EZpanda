from panda3d.core import DirectionalLight, NodePath
from scripts.EZpanda.EZnode import Node



class Sun(Node):
    __slots__=(
        'panda_node',
        'set_film_size',
        'show_frustum',
        'hide_frustum'
        )

    def __init__(self, size=(10,10), shadow_size=(512, 512), parent=None):
        Node.__init__(self, parent=parent, panda_node=NodePath( DirectionalLight('') ))

        #Assign a unique state key to this camera(light):
        ez._cam_count += 1
        self.panda_node.node().tag_state_key = 'cam' + str(ez._cam_count)

        self.panda_node.node().get_lens().set_near_far(1, 100)

        self.set_film_size = self.panda_node.node().get_lens().set_film_size
        self.set_film_size(*size)

        self.panda_node.node().set_shadow_caster(True, *shadow_size)

        self.show_frustum = self.panda_node.node().show_frustum
        self.hide_frustum = self.panda_node.node().hide_frustum

    def add_render_state(self, state, state_name):
        self.panda_node.node().set_tag_state(state_name, state.panda_node.get_state())

    def set_shadow_castor(self, width, height, dynamic=True):
        self.panda_node.node().set_shadow_caster(dynamic, width, height)

    @property
    def near(self):
        return self.panda_camera.node().get_lens().get_near()
    @near.setter
    def near(self, value):
        self.panda_camera.node().get_lens().set_near(value)

    @property
    def far(self):
        return self.panda_camera.node().get_lens().get_far()
    @far.setter
    def far(self, value):
        self.panda_camera.node().get_lens().set_far(value)