from panda3d.bullet import BulletWorld, BulletTriangleMesh
from panda3d.bullet import BulletRigidBodyNode, BulletGhostNode, BulletDebugNode
from panda3d.bullet import BulletConvexHullShape, BulletTriangleMeshShape, BulletPlaneShape, BulletSphereShape, BulletPlaneShape, BulletBoxShape, BulletCylinderShape, BulletCapsuleShape, BulletConeShape
from panda3d.core import NodePath, TransformState

from scripts.EZpanda.EZnode import Node



class Shapes:
    __slots__=()

    Sphere = BulletSphereShape
    Box = BulletBoxShape
    Capsule = BulletCapsuleShape
    Cylinder = BulletCylinderShape
    Plane = BulletPlaneShape
    Cone = BulletConeShape

    def make_convex_hull(self, EZnode):
        shape = BulletConvexHullShape()
        shape.add_geom( EZnode.panda_node.find_all_matches('**/+GeomNode').get_path(0).node().get_geom(0) )
        return shape

    def make_triangle_mesh(self, EZnode, dynamic=True):
        mesh = BulletTriangleMesh()
        mesh.add_geom( EZnode.panda_node.find_all_matches('**/+GeomNode').get_path(0).node().get_geom(0) )
        shape = BulletTriangleMeshShape(mesh, dynamic=dynamic)
        return shape



class RigidBody(Node):
    __slots__=(
        'physics_node',
        '_world'
        )

    def __init__(self, shape, parent=None, mass=1.0):
        self.physics_node = BulletRigidBodyNode('rigid_node')
        self.physics_node.add_shape(shape)
        self.physics_node.mass = mass
        Node.__init__(self, parent=parent, panda_node=NodePath(self.physics_node))

        self._world = None

    @property
    def kinematic(self):
        return self.physics_node.is_kinematic()
    @kinematic.setter
    def kinematic(self, bool_):
        self.physics_node.set_kinematic(bool_)

    @property
    def active(self):
        return self.physics_node.is_active()
    @active.setter
    def active(self, bool_):
        self.physics_node.force_active(bool_)

    @property
    def linear_velocity(self):
        return self.physics_node.get_linear_velocity()
    @linear_velocity.setter
    def linear_velocity(self, vector):
        self.physics_node.set_linear_velocity(vector)

    @property
    def angular_damping(self):
        return self.physics_node.get_angular_damping()
    @angular_damping.setter
    def angular_damping(self, value):
        self.physics_node.set_angular_damping(value)

    @property
    def linear_damping(self):
        return self.physics_node.get_linear_damping()
    @linear_damping.setter
    def linear_damping(self, value):
        self.physics_node.set_linear_damping(value)

    @property
    def mass(self):
        return self.physics_node.get_mass()
    @mass.setter
    def mass(self, value):
        self.physics_node.set_mass(value)

    @property
    def friction(self):
        return self.physics_node.get_friction()
    @friction.setter
    def friction(self, value):
        self.physics_node.set_friction(value)

    def delete(self):
        for child in self.panda_node.get_children():
            EZnode = child.get_python_tag('EZnode')
            if EZnode:
                EZnode.delete()

        self.parent = None
        self.panda_node.clear_python_tag('EZnode')
        if self._world:
            self._world.physics_world.remove_rigid_body(self.physics_node)

        self.panda_node.remove_node()



class GhostBody(Node):
    __slots__=(
        'physics_node',
        '_world'
        )

    def __init__(self, shape, parent=None):
        self.physics_node = BulletGhostNode('ghost_node')
        self.physics_node.add_shape(shape)
        Node.__init__(self, parent=parent, panda_node=NodePath(self.physics_node))

        self._world = None

    @property
    def kinematic(self):
        return self.physics_node.is_kinematic()
    @kinematic.setter
    def kinematic(self, bool_):
        self.physics_node.set_kinematic(bool_)

    def get_overlapping_nodes(self):
        nodes = []
        for node in self.physics_node.get_overlapping_nodes():
            nodes.append(node.get_python_tag('EZnode'))
        return nodes

    def delete(self):
        for child in self.panda_node.get_children():
            EZnode = child.get_python_tag('EZnode')
            if EZnode:
                EZnode.delete()

        self.parent = None
        self.panda_node.clear_python_tag('EZnode')
        if self._world:
            self._world.physics_world.remove_ghost(self.physics_node)
        self.panda_node.remove_node()




class Bodys:
    __slots__=()

    Rigid = RigidBody
    Ghost = GhostBody



class World:
    __slots__=(
        'physics_world',
        'update'
        )

    def __init__(self, gravity=(0,0,-9.81)):
        self.physics_world = BulletWorld()
        self.update = self.physics_world.do_physics
        self.physics_world.set_gravity(gravity)

    def add_body(self, body):
        if body._world:
            body._world.physics_world.remove_rigid_body(body.physics_node)
        self.physics_world.attach_rigid_body(body.physics_node)
        body._world = self

    def remove_body(self, body):
        self.physics_world.remove_rigid_body(body.physics_node)
        body._world = None

    def add_ghost(self, body):
        if body._world:
            body._world.physics_world.remove_ghost(body.physics_node)
        self.physics_world.attach_ghost(body.physics_node)
        body._world = self

    def remove_ghost(self, body):
        self.physics_world.attach_ghost(body.physics_node)
        body._world = None

    def ray_test_closest(self, fr, to, mask=ez.mask['ALL'] ):
        result = self.physics_world.ray_test_closest(fr, to, mask)
        if result.has_hit():
            hit = {
            'NODE': result.get_node().get_python_tag('EZnode'),
            'POS': result.get_hit_pos(),
            'NORMAL': result.get_hit_normal()
            }
            return hit
        return None

    def ray_test_all(self, fr, to, mask=ez.mask['ALL'] ):
        results = self.physics_world.ray_test_all(fr, to, mask)
        hits = []
        for result in results.get_hits():
            hit = {
            'NODE': result.get_node().get_python_tag('EZnode'),
            'POS': result.get_hit_pos(),
            'NORMAL': result.get_hit_normal()
            }
            hits.append(hit)
        return hits

    def sweep_test(self, convex_shape, fr, to, mask=ez.mask['ALL'], penetration=0):
        result = self.physics_world.sweep_test_closest(convex_shape, TransformState.make_pos(fr), TransformState.make_pos(to), mask, penetration)
        if result.has_hit():
            hit = {
            'NODE': result.get_node().get_python_tag('EZnode'),
            'POS': result.get_hit_pos(),
            'NORMAL': result.get_hit_normal()
            }
            return hit
        return None

    def contact_test(self, body):
        result = self.physics_world.contact_test(body.panda_node.node())
        hits = []
        for contact in result.get_contacts():
            hit = {
            'NODE1': contact.get_node0().get_python_tag('EZnode'),
            'NODE2': contact.get_node1().get_python_tag('EZnode')
            }
            hits.append(hit)
        return hits



class Physics:
    __slots__=()

    shapes = Shapes()
    bodys = Bodys()

    #Phyiscs world:
    World = World

    def enable_debug(self, world, render_node):
        node = BulletDebugNode('Debug')
        node.showWireframe(True)
        node.showConstraints(True)
        node.showBoundingBoxes(True)
        node.showNormals(True)
        node = render_node.panda_node.attach_new_node(node)
        node.show()
        world.physics_world.set_debug_node(node.node())
        return node

    def get_mask(self, body):
        return body.physics_node.get_into_collide_mask()

    def set_mask(self, body, mask):
        return body.physics_node.set_into_collide_mask(mask)

    def add_mask(self, body, mask):
        return body.physics_node.set_into_collide_mask(self.get_mask(body) | mask)

    def remove_mask(self, body, mask):
        return body.physics_node.set_into_collide_mask(self.get_mask(body) ^ mask)

    def has_mask(self, body, mask):
        return mask & self.get_mask(body) == mask