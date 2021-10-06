from scripts.EZpanda.EZnode import Node
from panda3d.core import Texture, GeomEnums, BoundingVolume, BoundingBox, BoundingSphere, RigidBodyCombiner, NodePath
from struct import pack_into



class SoftInstance(Node):
    __slots__=(
        '_mesh',
        '_instances'
        )

    def __init__(self, mesh, total_instances, parent=None):
        Node.__init__(self, panda_node=NodePath(RigidBodyCombiner('rbx')), parent=parent)
        self._instances = []
        for i in range(0, total_instances):
            model = ez.Model(mesh, parent=self)
            model.parent = self
            # Need to offset model from RigidBodyCombiner node or else the models become part of RBC itself when collect().
            model.x = i+1
            self._instances.append(model)
        self.panda_node.node().collect()

    def __getitem__(self, item):
        return self._instances[item]



class HardInstance(Node):
    __slots__=(
        '_mesh',
        '_total_instances',
        '_bounds',
        '_buffer',
        '_image_buffer'
        )

    def __init__(self, mesh, total_instances, boundsWHD, hpr=(0,0,0), parent=None):
        Node.__init__(self, parent=parent)
        self._mesh = NodePath( mesh.node().copy_subgraph() )
        self._mesh.set_hpr(hpr)
        self._mesh.flatten_strong()
        self._mesh.reparent_to(self.panda_node)
        self._total_instances = total_instances
        self._bounds = ez.Point3(boundsWHD)

        # Set the bounding volume:
        self._mesh.node().setBoundsType( BoundingVolume.BTBox )
        self._mesh.node().set_bounds( BoundingBox(-self._bounds*0.5, self._bounds*0.5) )
        self._mesh.node().set_final(True)

        self._buffer = Texture("I")
        self._buffer.setup_buffer_texture(self._total_instances*16, Texture.T_float, Texture.F_rgba32, GeomEnums.UH_static)
        self._image_buffer = memoryview(self._buffer.modify_ram_image())

        self._mesh.set_instance_count(self._total_instances)
        self._mesh.set_shader_input('texbuffer', self._buffer)


    def get_bounds(self):
        return self._bounds

    def show_bounds(self):
        self._mesh.show_bounds()

    def hide_bounds(self):
        self._mesh.hide_bounds()

    def get_total_instances(self):
        return self._total_instances

    def set_instance_pos(self, index, pos, size=1):
        x, y, z = pos
        pack_into('ffff', self._image_buffer, index*16,  x, y, z, size)
        self._buffer.modify_ram_image()

    def set_instances_pos(self, index_pos_size):
        for index, pos, size in index_pos_size:
            x, y, z = pos
            pack_into('ffff', self._image_buffer, index*16, x, y, z, size)
        self._buffer.modify_ram_image()

    def generate_random_pos(self, scale_min=1.0, scale_max=1.0):
        w, h, d = self._bounds*0.5
        for index in range(self._total_instances):
            pack_into('ffff', self._image_buffer, index*16, ez.random.uniform(-w, w), ez.random.uniform(-h, h), ez.random.uniform(-d, d), ez.random.uniform(scale_min, scale_max))
        self._buffer.modify_ram_image()




