from scripts.EZpanda.EZnode import Node




class Model(Node):
    __slots__=(
        'get_bounds',
        'get_tight_bounds',
        'show_bounds',
        'show_tight_bounds',
        'hide_bounds'
        )

    def __init__(self, mesh, parent=None):
        Node.__init__(self, panda_node=mesh, parent=parent)

        self.get_bounds = self.panda_node.get_bounds
        self.get_tight_bounds = self.panda_node.get_tight_bounds
        self.show_bounds = self.panda_node.show_bounds
        self.show_tight_bounds = self.panda_node.show_tight_bounds
        self.hide_bounds = self.panda_node.hide_bounds