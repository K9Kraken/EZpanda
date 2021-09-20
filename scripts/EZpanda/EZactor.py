from panda3d.core import ShaderAttrib
from direct.actor.Actor import Actor as PandaActor
from scripts.EZpanda.EZmodel import Model



class Actor(Model):
    __slots__=(
        'play',
        'loop',
        'stop',
        'get_animations'
        )
    def __init__(self, mesh, animations=None, parent=None):

        Model.__init__(self, PandaActor(mesh, animations), parent=parent)

        #Enable hardware animation: (Shader needs to transform vertex animations)
        attr = ShaderAttrib.make()
        attr = attr.set_flag(ShaderAttrib.F_hardware_skinning, True)
        self.panda_node.set_attrib(attr)

        self.play = self.panda_node.play
        self.loop = self.panda_node.loop
        self.stop = self.panda_node.stop
        self.get_animations = self.panda_node.get_anim_names


