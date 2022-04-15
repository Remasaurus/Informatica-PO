import pygame

from components.WallJump import WallJump
from entities.Entity import Entity
from components.Dash import Dash
from components.jump import Jump
from components.move import Move
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
        self.spikeable = True
        self.size.update(16, 26)
        
    
    @property
    def frame(self):
        return "player"
    
    def hit(self):
        pass
    
    def draw(self, surface, camera, spritesheet): 
        if self.scale == (1, 1):
            frame = self.components["Animator"].get_frame()
            if frame.name in spritesheet.anims:
                spritesheet.draw(frame.name, surface, self.pos.x -
                         camera.pos.x, self.pos.y - camera.pos.y, frame.time, self.flip)
            else:
                spritesheet.draw(frame.name, surface, self.pos.x -
                         camera.pos.x, self.pos.y - camera.pos.y, self.flip)
        else:
            buffer = pygame.Surface(self.size, pygame.SRCALPHA)
            frame = self.components["Animator"].get_frame()
            if frame.name in spritesheet.anims:
                spritesheet.draw(frame.name, buffer, 0, 0, frame.time, self.flip)
            else:
                spritesheet.draw(frame.name, buffer, 0, 0, self.flip)
            
            inflate = self.scale - (1, 1)
            inflate.x *= self.size.x
            inflate.y *= self.size.y
            rect = pygame.Rect(self.pos - camera.pos, self.size).inflate(inflate.x, inflate.y)
            
            surface.blit(pygame.transform.scale(buffer, rect.size), rect.topleft)

