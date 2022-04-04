import pygame
from entities.Entity import Entity
from components.physics import Physics
from components.Follower import Follower

class Helper(Entity):
    def __init__(self):
        super().__init__()
        self.following = None
        self.size = pygame.Vector2(8, 8)
        self.add_component(Physics())
        self.add_component(Follower())
    
    def follow(self, entity):
        self.following = entity
    