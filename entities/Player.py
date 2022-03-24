import pygame
from entities.Entity import Entity


class Player(Entity):
    """Player class that overwrites the draw function."""
    
    @property
    def frame(self):
        return "player"
    
    def draw(self, surface, camera, spritesheet):   
        buffer = pygame.Surface(self.size, pygame.SRCALPHA)
        spritesheet.draw(self.frame, buffer, 0, 0)
        
        inflate = self.scale - (1, 1)
        inflate.x *= self.size.x
        inflate.y *= self.size.y
        rect = pygame.Rect(self.pos - camera.pos, self.size).inflate(inflate.x, inflate.y)
        
        surface.blit(pygame.transform.scale(buffer, rect.size), rect.topleft)

    def draw(self, surface, camera, spritesheet):
        spritesheet.draw(self.frame, surface, self.pos.x -
                         camera.pos.x, self.pos.y - camera.pos.y)
