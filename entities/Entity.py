import pygame


class Entity():
    """Base class for all entities"""
    def __init__(self):
        self.pos = pygame.Vector2(0, 0)
        self.vel = pygame.Vector2(0, 0)
        self.size = pygame.Vector2(16, 16)
        self.life_time = 0
        self.components = dict()
        self.scale = pygame.Vector2(1, 1)

    def add_component(self, component):
        """Adds component to entity with classname as key."""
        self.components[type(component).__name__] = component

    def obstruct(self, side):
        """Tell components a collision event happened."""
        for component in self.components.values():
            component.obstruct(self, side)

    def draw(self, surface, camera, spritesheet):
        """Draw square on the surface at positon."""
        inflate = self.scale - (1, 1)
        inflate.x *= self.size.x
        inflate.y *= self.size.y
        
        pygame.draw.rect(surface, pygame.Color(255, 105, 180),
            pygame.Rect(self.pos - camera.pos, self.size)
                         .inflate(inflate.x, inflate.y)
        )

    def update(self, delta_time, level):
        """Calls updates on all the components."""
        for component in self.components.values():
            component.update(self, delta_time, level)

        self.life_time += delta_time
