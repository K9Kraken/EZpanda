from panda3d.core import CollisionTraverser, CollisionHandlerQueue
from panda3d.core import CollisionNode
from panda3d.core import CollisionPlane, CollisionSphere, CollisionCapsule, CollisionBox
from panda3d.core import CollisionRay, CollisionLine, CollisionSegment
from panda3d.core import NodePath, Point3
from panda3d.core import Plane as PandaPlane
from scripts.EZpanda.EZnode import Node


#Shapes:
class Plane(Node):
    __slots__=(
        'collision_node'
        )

    def __init__(self, face_normal, pos, parent=None):
        self.collision_node = CollisionNode('Cnode')
        self.collision_node.set_from_collide_mask(0)
        self.collision_node.add_solid(CollisionPlane(PandaPlane( face_normal, pos )))
        Node.__init__(self, parent=parent, panda_node=NodePath(self.collision_node) )



class Sphere(Node):
    __slots__=(
        'collision_node'
        )

    def __init__(self, radius, origin=(0,0,0), parent=None):
        self.collision_node = CollisionNode('Cnode')
        self.collision_node.set_from_collide_mask(0)
        self.collision_node.add_solid(CollisionSphere( origin, radius ))
        Node.__init__(self, parent=parent, panda_node=NodePath(self.collision_node) )



class Box(Node):
    __slots__=(
        'collision_node'
        )

    def __init__(self, bounds, origin=(0,0,0), parent=None):
        self.collision_node = CollisionNode('Cnode')
        self.collision_node.set_from_collide_mask(0)
        self.collision_node.add_solid(CollisionBox( origin, *bounds))
        Node.__init__(self, parent=parent, panda_node=NodePath(self.collision_node) )



class Capsule(Node):
    __slots__=(
        'collision_node'
        )

    def __init__(self, origin, end, radius, parent=None):
        self.collision_node = CollisionNode('Cnode')
        self.collision_node.set_from_collide_mask(0)
        self.collision_node.add_solid(CollisionCapsule( *origin, *end, radius ))
        Node.__init__(self, parent=parent, panda_node=NodePath(self.collision_node) )



class Shapes:
    __slots__=()

    Plane = Plane
    Sphere = Sphere
    Box = Box
    Capsule = Capsule #Does not collide in to the capsule.



#Rays:
class Ray(Node):
    __slots__=(
        '_collision_node',
        '_collision_ray'
        )

    def __init__(self, pos=(0,0,0), direction=(0,0,1), parent=None):
        self._collision_node = CollisionNode('Cnode')
        self._collision_node.set_from_collide_mask(0)
        self._collision_ray = CollisionRay() #CollisionRay( *origin, *direction)
        self._collision_node.add_solid(self._collision_ray)
        Node.__init__(self, parent=parent, panda_node=NodePath(self._collision_node) )
        self.pos = pos
        self.direction = direction

    @property
    def direction(self):
        return self._collision_ray.get_direction()
    @direction.setter
    def direction(self, dir_):
        self._collision_ray.set_direction(dir_)



class Line(Node):
    __slots__=(
        '_collision_node',
        '_collision_line'
        )

    def __init__(self, pos=(0,0,0), direction=(0,0,1), parent=None):
        self._collision_node = CollisionNode('Cnode')
        self._collision_node.set_from_collide_mask(0)
        self._collision_line = CollisionLine()
        self._collision_node.add_solid(self._collision_line)
        Node.__init__(self, parent=parent, panda_node=NodePath(self._collision_node) )
        self.pos = pos
        self.direction = direction

    @property
    def direction(self):
        return self._collision_line.get_direction()
    @direction.setter
    def direction(self, dir_):
        self._collision_line.set_direction(dir_)



class Segment(Node):
    __slots__=(
        '_collision_node',
        '_collision_segment'
        )

    def __init__(self, pos=(0,0,0), to=(0,0,1), parent=None):
        self._collision_node = CollisionNode('Cnode')
        self._collision_node.set_from_collide_mask(0)
        self._collision_segment = CollisionSegment()
        self._collision_node.add_solid(self._collision_segment)
        Node.__init__(self, parent=parent, panda_node=NodePath(self._collision_node) )
        self.pos = pos
        self.to = to

    @property
    def to(self):
        return self._collision_segment.get_point_b()
    @to.setter
    def to(self, pos):
        self._collision_segment.set_point_b(pos)



class Rays:
    __slots__=()

    Ray = Ray
    Line = Line
    Segment = Segment



#Handlers:
class Handler():
    __slots__=(
        'panda_handler',
        'panda_traverser',
        )

    def __init__(self):
        self.panda_handler = CollisionHandlerQueue()
        self.panda_traverser = CollisionTraverser('handler')

    def add_collider(self, EZnode):
        self.panda_traverser.add_collider(EZnode.panda_node, self.panda_handler)
        EZnode._colliders.append(self)

    def remove_collider(self, EZnode):
        self.panda_traverser.remove_collider(EZnode.panda_node)
        EZnode._colliders.remove(self)

    def get_collisions(self, traverse_node, relative_space=ez.panda_showbase.render):
        collisions = []
        self.panda_traverser.traverse(traverse_node.panda_node)
        if self.panda_handler.get_num_entries() > 0:
            self.panda_handler.sort_entries()
            for entry in self.panda_handler.get_entries():
                collision = {
                #'FROM':   entry.get_from_node_path().find_net_tag('panda_node').get_python_tag('EZnode'),
                'FROM':   entry.get_from_node_path().get_python_tag('EZnode'),
                'INTO':   entry.get_into_node_path().find_net_tag('panda_node').get_python_tag('EZnode'),
                'POS':    entry.get_surface_point(relative_space),
                'NORMAL': entry.get_surface_normal(relative_space)
                }
                collisions.append(collision)
            return collisions
        return None



class MousePicker:
    __slots__=(
        '_camera',
        '_cray',
        '_handler',
        '_ctraverser',
        )

    def __init__(self, camera, mask=ez.mask[1]):
        self._camera = camera
        self._cray = CollisionRay()
        cnode = CollisionNode('mouse_ray')
        cnode.set_from_collide_mask(mask)
        cnode.set_into_collide_mask(0)
        cnode.add_solid(self._cray)
        self._handler = CollisionHandlerQueue()
        self._ctraverser = CollisionTraverser('mouse_traverser')
        self._ctraverser.add_collider(camera.panda_node.attach_new_node(cnode), self._handler)

    def get_hit(self, traverse_node, relative_space=ez.panda_showbase.render):
        pos = ez.panda_showbase.mouseWatcherNode.get_mouse()
        self._cray.set_from_lens(self._camera.panda_node.node(), pos.get_x(), pos.get_y())
        self._ctraverser.traverse(traverse_node.panda_node)
        if self._handler.get_num_entries():
            self._handler.sort_entries()
            hit = self._handler.get_entry(0)
            collision = {
            'NODE':   hit.get_into_node_path().find_net_tag('panda_node').get_python_tag('EZnode'),
            'POS':    hit.get_surface_point(relative_space),
            'NORMAL': hit.get_surface_normal(relative_space)
            }
            return collision
        else:
            return None



class MousePickre2D:
    __slots__=(
        '_cray',
        '_ctraverser',
        '_handler'
        )

    def __init__(self, mask=ez.mask[1]):
        self._cray = CollisionRay()
        cnode = CollisionNode('mouse_2d_ray')
        cnode.set_from_collide_mask(mask)
        cnode.set_into_collide_mask(0)
        cnode.add_solid(self._cray)
        self._ctraverser = CollisionTraverser('mouse_3d_traverser')
        self._handler = CollisionHandlerQueue()
        self._ctraverser.add_collider(ez.panda_showbase.aspect2d.attach_new_node(cnode), self._handler)

    def get_hit(self, traverse_node, depth=100):
        x, y = ez.mouse.pos
        self._cray.set_origin( (x, y, 0) )
        self._cray.set_direction( (0, 0, -1) )
        self._ctraverser.traverse(traverse_node.panda_node)
        if self._handler.get_num_entries():
            self._handler.sort_entries()
            hit = self._handler.get_entry(0)
            collision = {
            'NODE':   hit.get_into_node_path().find_net_tag('panda_node').get_python_tag('EZnode'),
            'POS':    hit.get_surface_point(ez.panda_showbase.aspect2d),
            'NORMAL': hit.get_surface_normal(ez.panda_showbase.aspect2d)
            }
            return collision
        else:
            return None



class Collision:
    __slots__=()

    #Collision shapes:
    shapes = Shapes()

    #Rays: (These only collide in to others)
    rays = Rays()

    #Collision handler:
    Handler = Handler

    #Class used for mouse clicking on objects:
    MousePicker = MousePicker
    MousePickre2D = MousePickre2D

    def get_mask(self, EZnode):
        return EZnode.panda_node.get_collide_mask()

    def set_mask(self, EZnode, mask):
        EZnode.panda_node.set_collide_mask(mask)

    def add_mask(self, EZnode, mask):
        EZnode.panda_node.set_collide_mask(self.get_mask(EZnode) | mask)

    def remove_mask(self, EZnode, mask):
        EZnode.panda_node.set_collide_mask(self.get_mask(EZnode) ^ mask)

    def has_mask(self, EZnode, mask):
        return mask & self.get_mask(EZnode) == mask

    #Only works on Collision shapes and Rays:
    def get_target_mask(self, EZnode):
        return EZnode.panda_node.node().get_from_collide_mask()

    def set_target_mask(self, EZnode, mask):
        EZnode.panda_node.node().set_from_collide_mask(mask)

    def add_target_mask(self, EZnode, mask):
        EZnode.panda_node.node().set_from_collide_mask(self.get_target_mask(EZnode) | mask)

    def remove_target_mask(self, EZnode, mask):
        EZnode.panda_node.node().set_from_collide_mask(self.get_target_mask(EZnode) ^ mask)

    def has_target_mask(self, EZnode, mask):
        return mask & self.get_target_mask(EZnode) == mask

