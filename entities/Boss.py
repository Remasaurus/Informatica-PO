import pygame
from entities.Entity import Entity

class Boss(Entity):
    def __init__(self):
        super().__init__()
        self.vonerable = False
        self.gem_rect = pygame.Rect(0, 0, 10, 10)