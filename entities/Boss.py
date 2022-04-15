import pygame
from components.Animator import Animator
from entities.Entity import Entity
from components.Physics import Physics
from components.Boss import BossAI

class Boss(Entity):
    def __init__(self):
        super().__init__()
        self.size = pygame.Vector2(64, 64)
        self.add_component(BossAI())
        self.add_component(Physics())
        self.add_component(Animator())
        
        self.vulnerable = False
        self.lives = 3
        
    def hit(self, level):
        self.lives -= 1
        if self.lives <= 0:
            level.finished = True
    
    def draw(self, surface, camera, spritesheet):
        spritesheet.draw(self.components["Animator"].get_frame().name, surface, self.pos.x - camera.pos.x, self.pos.y - camera.pos.y, self.flip)
        