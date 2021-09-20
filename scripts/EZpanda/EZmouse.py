class Mouse:
    __slots__=(
        '_system_cursor',
        'has_mouse'
        )

    def __init__(self):
        self._system_cursor = ez.window.panda_winprops.get_cursor_filename()
        self.has_mouse = ez.panda_showbase.mouseWatcherNode.has_mouse

    def hide(self):
        ez.window.panda_winprops.set_cursor_hidden(True)
        ez.panda_showbase.win.request_properties(ez.window.panda_winprops)

    def show(self):
        ez.window.panda_winprops.set_cursor_hidden(False)
        ez.panda_showbase.win.request_properties(ez.window.panda_winprops)

    @property
    def cursor(self):
        return ez.window.panda_winprops.get_cursor_filename()
        ez.panda_showbase.win.request_properties(ez.window.panda_winprops)
    @cursor.setter
    def cursor(self, cursor):
        if cursor:
            ez.window.panda_winprops.set_cursor_filename(cursor)
        else:
            ez.window.panda_winprops.set_cursor_filename(self._system_cursor)
        ez.panda_showbase.win.request_properties(ez.window.panda_winprops)

    @property
    def mouse_pos(self):
        return ez.panda_showbase.mouseWatcherNode.get_mouse()

    @property
    def pos(self):
        # Convert mouse coordinates to aspect2D coordinates:
        mpos = ez.panda_showbase.mouseWatcherNode.get_mouse()
        pos = aspect2d.get_relative_point(render, (mpos.x, mpos.y, 0))
        return pos.xy
    @pos.setter
    def pos(self, pos):
        # Have to convert aspect2D position to window coordinates:
        x, y = pos
        w, h = ez.panda_showbase.win.get_size()
        cpos = ez.panda_showbase.camera2d.get_pos()
        L, R, T, B = ez.window.get_aspect2D_edges()

        # Get aspect2D size:
        aw = R-L
        ah = T-B

        # Get mouse pos equivalent to window cordinates:
        mx = x+R
        my = abs(y+B)

        # Convert the mouse pos to window position:
        x = mx/aw*w
        y = my/ah*h

        ez.panda_showbase.win.move_pointer(0, round(x), round(y))