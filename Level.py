import pygame
from Collider import Collider
from Compositor import Compositor
from ParticleSystem import ParticleSystem


class Level():
    def __init__(self):
        self.entities = []
        self.collider = Collider(0)
        self.total_time = 0
        self.compositor = Compositor()
        self.gravity = 10
        self.particle_system = ParticleSystem()

    def update(self, delta_time):
        """Update all tiles and entities in the level."""
        for entity in self.entities:
            entity.update(delta_time, self)

        self.particle_system.update(delta_time)

    def draw(self, surface, camera):
        """Draw all tiles and entities in the level."""
        self.compositor.draw(surface, camera)
        self.particle_system.draw(surface, camera)
