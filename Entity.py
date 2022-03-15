import pygame


class Entity():
    """Base class for all entities"""

    def __init__(self):
        self.pos = pygame.Vector2(0, 0)
        self.vel = pygame.Vector2(0, 0)
        self.size = pygame.Vector2(16, 16)
        self.life_time = 0
        self.components = dict()

    def add_component(self, component):
        self.components[type(component).__name__] = component

    def obstruct(self, side):
        for component in self.components.values():
            component.obstruct(self, side)

    def draw(self, surface, camera, spritesheet):
        pygame.draw.rect(surface, pygame.Color(255, 105, 180), pygame.Rect(
            self.pos.x - camera.pos.x, self.pos.y - camera.pos.y, self.size.x, self.size.y))

    def update(self, delta_time, level):
        for component in self.components.values():
            component.update(self, delta_time, level)

        self.life_time += delta_time
