import pygame
from particles.Particle import Particle


FIREBALL = pygame.image.load("./img/fireball.png")


class FireBall(Particle):
    SPEED = 500
    
    def __init__(self, pos, dir):
        super().__init__(pos)
        FIREBALL.convert_alpha()
        self.dir = dir
        self.size = FIREBALL.get_size()
    
    def draw(self, surface, camera):
        surface.blit(FIREBALL, self.pos - camera.pos)
        
    def update(self, delta_time):
        self.pos.x += self.dir * self.SPEED * delta_time
        
    
        
