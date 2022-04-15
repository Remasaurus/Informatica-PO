import pygame
from ParticleSystem import ParticleSystem
from Camera import Camera
from Compositor import Compositor
from Collider import Collider


class Level():
    """Contains all objects that are needed in a level."""
    def __init__(self):
        self.entities = []
        self.compositor = Compositor()
        self.collider = Collider(0)
        self.total_time = 0
        self.gravity = 10
        self.particle_system = ParticleSystem()
        self.camera = Camera()

    def update(self, delta_time):
        """Update all tiles and entities in the level."""
        for entity in self.entities:
            entity.update(delta_time, self)

        self.particle_system.update(delta_time)
        self.collider.update(delta_time, self)
        self.camera.focus(self.entities[0])

    def draw(self, surface):
        """Draw all tiles and entities in the level."""
        draw_surface = pygame.Surface(self.camera.size)
        
        self.compositor.draw(draw_surface, self.camera)
        self.particle_system.draw(draw_surface, self.camera)
        
        pygame.transform.scale(draw_surface, surface.get_size(), surface)
