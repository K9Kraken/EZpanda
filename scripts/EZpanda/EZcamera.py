from panda3d.core import Camera as PandaCamera, PerspectiveLens, OrthographicLens, NodePath, Point3
from panda3d.core import WindowProperties, FrameBufferProperties, GraphicsPipe, Texture, GraphicsOutput
from scripts.EZpanda.EZnode import Node


class Camera(Node):
    __slots__=(
        'lens',
        'panda_node',
        'set_aspect_ratio',
        '_depth_map'
        )

    ORTHO = OrthographicLens
    PERSPECTIVE = PerspectiveLens
    def __init__(self, lens=PERSPECTIVE, parent=None):
        self.lens = lens()
        Node.__init__(self, parent=parent, panda_node=NodePath(PandaCamera( "cam", self.lens )))

        # Assign a unique state key to the camera:
        ez._cam_count += 1
        self.panda_node.node().tag_state_key = 'cam' + str(ez._cam_count)
        self.set_aspect_ratio = self.lens.set_aspect_ratio

        # width, height = ez.window.get_size()
        self.set_aspect_ratio(ez.window.get_aspect_ratio())

        self._depth_map = None
    def get_depth_map(self):
        return self._depth_map

    def get_projected_ray(self, aspect2D_pos):
        near = Point3()
        far = Point3()

        # Convert from aspect2D to mouse coordinates:
        x, y = aspect2D_pos
        pos = render.get_relative_point(aspect2d, (x, y, 0) )

        self.lens.extrude(pos, near, far)
        fr = ez.panda_showbase.render.get_relative_point(self.panda_node, near)
        to = ez.panda_showbase.render.get_relative_point(self.panda_node, far)
        return fr, to

    def add_render_state(self, state, state_name):
        self.panda_node.node().set_tag_state(state_name, state.panda_node.get_state())

    def create_depth_map(self):
        win_props = WindowProperties.size(*ez.window.get_size())
        frame_props = FrameBufferProperties()
        frame_props.setRgbColor(1)
        frame_props.setAlphaBits(1)
        frame_props.set_depth_bits(1)

        z_buffer = ez.panda_showbase.graphics_engine.make_output( ez.panda_showbase.pipe, "offscreen buffer", -2, frame_props, win_props, GraphicsPipe.BF_refuse_window, ez.panda_showbase.win.get_gsg(), ez.panda_showbase.win)
        z_buffer.make_display_region(0, 1, 0, 1).set_camera(self.panda_node)
        depth_map = Texture()
        z_buffer.add_render_texture(depth_map, GraphicsOutput.RTM_bind_or_copy, GraphicsOutput.RTP_depth)
        self._depth_map = depth_map

        return depth_map

    @property
    def fov(self):
        return self.lens.get_fov().x
    @fov.setter
    def fov(self, value):
        self.lens.set_fov(value)

    @property
    def vfov(self):
        return self.lens.get_fov().y
    @vfov.setter
    def vfov(self, value):
        self.lens.set_fov(self.fov, value)

    @property
    def near(self):
        return self.lens.get_near()
    @near.setter
    def near(self, value):
        self.lens.set_near(value)

    @property
    def far(self):
        return self.lens.get_far()
    @far.setter
    def far(self, value):
        self.lens.set_far(value)