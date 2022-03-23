import pygame
from entities.Entity import Entity


class Player(Entity):
    """Player class that overwrites the draw function."""
        
    @property
    def frame(self):
        return "player"
    
    def draw(self, surface, camera, spritesheet):
        spritesheet.draw(self.frame, surface, self.pos.x -
                         camera.pos.x, self.pos.y - camera.pos.y)
