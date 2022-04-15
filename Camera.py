import math
import random
import pygame

def clamp(minimum, maximum, val):
    """Return the value clamped between minimum and maximum."""
    return max(minimum, min(maximum, val))


class Camera():
    """Container for the screensize and pos."""
    def __init__(self, size = (0, 0), pos = (0, 0)) -> None:
        self.size = pygame.Vector2(size) or pygame.Vector2(pygame.display.get_window_size())
        self.pos = pygame.Vector2(pos)
        self.shake_time = 0
        self.shake_intensity = 0
        self.clock = pygame.time.Clock()
        self.minX = 0
        self.maxX = 100000
        self.minY = 0
        self.maxY = 100000
        
    def shake(self, duration: float, intensity: int):
        """Shakes the camera for a given duration."""
        self.shake_time = duration
        self.shake_intensity = intensity
        self.clock.tick()
        
        
    @property
    def aspect_ratio(self):
        return self.size.x/self.size.y
        
    def focus(self, entity):
        """Positions camera at the entities location."""
        offset = [0, 0]
        if self.shake_time > 0:
            self.shake_time -= self.clock.tick()/1000
            offset = [random.randint(-self.shake_intensity, self.shake_intensity),
                      random.randint(-self.shake_intensity, self.shake_intensity)]
            
        # TODO: Make camera move in front of the player
        self.pos.x = clamp(self.minX, self.maxX, entity.pos.x - 320 + offset[0])
        self.pos.y = clamp(self.minY, self.maxY, entity.pos.y - 180 + offset[1])
        
        
        
