import pygame
from entities.Entity import Entity
from components.physics import Physics
from components.Boss import BossAI

class Boss(Entity):
    def __init__(self):
        super().__init__()
        self.vonerable = False
        self.gem_rect = pygame.Rect(0, 0, 10, 10)
        self.size = pygame.Vector2(64, 64)
        self.add_component(BossAI())
        self.add_component(Physics())