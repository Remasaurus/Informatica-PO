import pygame
from particles.Particle import Particle


FIREBALL = pygame.image.load("./img/fireball.png")


class FireBall(Particle):
    def __init__(self, pos, dir):
        super().__init__(pos)
        self.dir = dir
    
    def draw(self, surface, camera):
        surface.blit(FIREBALL, self.pos - camera)
        
    def update(self, delta_time):
        self.pos.x += self.dir * 10
        
    
        
