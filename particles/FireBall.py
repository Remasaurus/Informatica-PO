import pygame
from particles.Particle import Particle


FIREBALL = pygame.image.load("./img/fireball.png")


class FireBall(Particle):
    def draw(self, surface, camera):
        surface.blit(FIREBALL, self.pos - camera)
    
        
