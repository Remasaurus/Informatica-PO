import pygame
from particles.Particle import Particle

dust = pygame.image.load("./img/dust.png")

class DustParticle(Particle):
    def __init__(self, pos):
        super().__init__(pos)
        self.alpha = 255
        self.buffer = dust
        
    def update(self, delta_time):
        self.alpha -= delta_time * 500
        self.pos.y -= delta_time * 20
        
        if self.alpha < 0:
            self.alive = False
            self.alpha = 0
        
    
    def draw(self, surface, camera):
        self.buffer.set_alpha(self.alpha)
        
        surface.blit(self.buffer, (
            self.pos.x - camera.pos.x - 2.5, self.pos.y - camera.pos.y - 2.5,
        ))
        