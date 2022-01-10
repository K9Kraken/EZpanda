from panda3d.core import WindowProperties, ClockObject



class Window:
    __slots__=(
        'panda_winprops',
        'get_display_modes',
        '_aspect2D_edges',
        '_show_fps'
        )

    def __init__(self):
        self.panda_winprops = WindowProperties()

        self.get_display_modes = ez.panda_showbase.pipe.get_display_information().get_display_modes

        self._show_fps = False

        self._aspect2D_edges = None

    def get_size(self):
        return self.panda_winprops.get_size()

    def get_aspect_ratio(self):
        w, h = self.panda_winprops.get_size()
        return w/h

    def get_aspect2D_edges(self):
        return self._aspect2D_edges

    def get_display_mode(self, int_=0):
        display = ez.panda_showbase.pipe.get_display_information()
        width = display.get_display_mode_width(int_)
        height = display.get_display_mode_height(int_)
        rate = display.get_display_mode_refresh_rate(int_)
        return width, height, rate

    def set_display(self, width, height, rate=60):
        self.panda_winprops.set_size(width, height)
        self.set_max_fps(rate)
        ez.panda_showbase.win.request_properties(self.panda_winprops)

        # Setup the aspect2D edges
        w, h = self.panda_winprops.get_size()
        size = ez.panda_showbase.cam2d.node().get_lens().get_film_size().get_x()
        cpos = ez.panda_showbase.camera2d.get_pos()
        ratio = w/h
        size = size*0.5

        if ratio >= size:
            L = cpos.x-ratio*size
            R = cpos.x+ratio*size
            T = cpos.y+size
            B = cpos.y-size
        else:
            L = cpos.x-size
            R = cpos.x+size
            T = cpos.y+size/ratio
            B = cpos.y-size/ratio

        self._aspect2D_edges = L, R, T, B

    def set_max_fps(self, int_):
        int_ = max(int_, 20)
        globalClock.set_mode(ClockObject.MLimited)
        globalClock.set_frame_rate(int_)

    @property
    def fullscreen(self):
        return self.panda_winprops.get_fullscreen()
    @fullscreen.setter
    def fullscreen(self, bool_):
        self.panda_winprops.set_fullscreen(bool_)
        ez.panda_showbase.win.request_properties(self.panda_winprops)

    @property
    def show_fps(self):
        return self.__show_fps
    @show_fps.setter
    def show_fps(self, bool_):
        ez.panda_showbase.set_frame_rate_meter(bool_)
        self._show_fps = bool_

    @property
    def background_color(self):
        return tuple(ez.panda_showbase.get_background_color().xyz)
    @background_color.setter
    def background_color(self, color):
        ez.panda_showbase.set_background_color(*color)