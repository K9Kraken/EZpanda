

class TextureBuffer:
    __slots__=(
        'panda_texture_buffer',
        'display_region',
        'set_clear_depth',
        'get_texture',
        '_background_color'
        )

    def __init__(self, width, height, display_region=(0,1,0,1), name="Texture Buffer"):
        self.panda_texture_buffer = ez.panda_showbase.win.make_texture_buffer(name, width, height)
        self.display_region = self.panda_texture_buffer.make_display_region(*display_region)
        self.panda_texture_buffer.set_sort(-100)

        self.set_clear_depth = self.display_region.set_clear_depth_active
        self.get_texture = self.panda_texture_buffer.get_texture

        self._background_color = (1,1,1,1)
        self.background_color = (1,1,1,1)

    @property
    def camera(self):
        return self.display_region.camera
    @camera.setter
    def camera(self, camera):
        camera.set_aspect_ratio(ez.panda_showbase.get_aspect_ratio( self.panda_texture_buffer ))
        self.display_region.camera = camera.panda_node

    @property
    def background(self):
        return self.display_region.is_any_clear_active()
    @background.setter
    def background(self, bool_):
        if bool_:
            self.display_region.set_clear_color_active(True)
        else:
            self.display_region.set_clear_color_active(False)

    @property
    def background_color(self):
        return self._background_color
    @background_color.setter
    def background_color(self, color):
        self._background_color = color
        self.display_region.set_clear_color(color)

    def __del__(self):
        self.panda_texture_buffer.remove_all_display_regions()

