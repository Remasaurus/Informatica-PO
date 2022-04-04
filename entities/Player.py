import pygame
from components.WallJump import WallJump
from entities.Entity import Entity
from components.Dash import Dash
from components.Jump import Jump
from components.Move import Move
from components.physics import Physics
from components.WallSlide import WallSlide
from components.CoinCollector import CoinCollector

class Player(Entity):
    """Player class that overwrites the draw function."""
    def __init__(self):
        super().__init__()
        self.add_component(Dash())
        self.add_component(Physics())
        self.add_component(Move())
        self.add_component(Jump())
        self.add_component(WallSlide())
        self.add_component(CoinCollector())
        self.add_component(WallJump())
    
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
