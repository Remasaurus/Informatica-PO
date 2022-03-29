import pygame
from entities.Entity import Entity


class Helper(Entity):
    def __init__(self):
        super().__init__()
        self.following = None
        self.size = pygame.Vector2(8, 8)
    
    def follow(self, entity):
        self.following = entity
    