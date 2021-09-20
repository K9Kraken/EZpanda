from panda3d.core import LineSegs, NodePath
from scripts.EZpanda.EZnode import Node



class Line(Node):
    __slots__=(
        'panda_line',
        '_line_node',
        'move_to',
        'set_color',
        'set_thickness',
        'draw_to',
        'reset'
        )

    def __init__(self, parent=None):
        Node.__init__(self, parent=parent, panda_node=NodePath(''))
        self.panda_line = LineSegs()
        self._line_node = NodePath('')

        self.move_to = self.panda_line.move_to
        self.set_color = self.panda_line.set_color
        self.set_thickness = self.panda_line.set_thickness
        self.draw_to = self.panda_line.draw_to
        self.reset = self.panda_line.reset

    def create(self):
        self._line_node.remove_node()
        self._line_node = NodePath(self.panda_line.create())
        self._line_node.reparent_to(self.panda_node)


