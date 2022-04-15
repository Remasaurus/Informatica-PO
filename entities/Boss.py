import pygame
from entities.Entity import Entity
from components.Physics import Physics
from components.Boss import BossAI

class Boss(Entity):
    def __init__(self):
        super().__init__()
        self.size = pygame.Vector2(64, 64)
        self.add_component(BossAI())
        self.add_component(Physics())
        self.vulnerable = False
        