import pygame
from Collider import Collider
from Compositor import Compositor
from ParticleSystem import ParticleSystem
from Camera import Camera


class Level():
    def __init__(self):
        self.entities = []
        self.collider = Collider(0)
        self.total_time = 0
        self.compositor = Compositor()
        self.gravity = 10
        self.particle_system = ParticleSystem()
        self.camera = Camera()

    def update(self, delta_time):
        """Update all tiles and entities in the level."""
        for entity in self.entities:
            entity.update(delta_time, self)

        self.particle_system.update(delta_time)
        
        self.camera.focus(self.entities[0])

    def draw(self, surface):
        """Draw all tiles and entities in the level."""
        self.compositor.draw(surface, self.camera)
        self.particle_system.draw(surface, self.camera)
