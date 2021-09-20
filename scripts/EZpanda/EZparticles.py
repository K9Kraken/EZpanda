from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ParticleEffect import Particles as PandaParticles
from direct.interval.ParticleInterval import ParticleInterval
from panda3d.physics import BaseParticleRenderer, PointParticleRenderer, BaseParticleEmitter

from scripts.EZpanda.EZnode import Node



class Particle(Node):
    __slots__=(
        'panda_node',
        '_render_parent',
        'on',
        'off',
        'disable'
        )

    def __init__(self, config, parent=None, render_parent=None):
        self.panda_node = ParticleEffect()
        self.panda_node.load_config(ez.PATH+'particles/'+config)
        Node.__init__(self, parent=parent, panda_node=self.panda_node)

        self._render_parent = render_parent
        if render_parent:
            self.render_parent = render_parent

        self.on = self.panda_node.soft_start
        self.off = self.panda_node.soft_stop
        self.disable = self.panda_node.disable

    def enable(self):
        if self._parent:
           self.parent = self._parent
        if self._render_parent:
            self.render_parent = self._render_parent
        self.panda_node.enable()

    @property
    def render_parent(self):
        return self._render_parent
    @render_parent.setter
    def render_parent(self, EZnode):
        for particle in self.panda_node.get_particles_list():
            particle.set_render_parent(EZnode.panda_node)
        self._render_parent = EZnode



class Particles:
    __slots__=()

    Particle = Particle

    def make_interval(self, particle, duration, parent, render_parent):
        return ParticleInterval(particle.panda_node, parent.panda_node, worldRelative=False, renderParent=render_parent.panda_node, duration=duration)