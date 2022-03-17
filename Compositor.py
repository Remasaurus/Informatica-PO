import pygame
from Camera import Camera


class Compositor():
    """Container around all layers in a scene."""

    def __init__(self):
        self.layers = []

    def draw(self, surface: pygame.Surface, camera: Camera):
        """Calls every layers' draw method."""
        for layer in self.layers:
            layer.draw(surface, camera)
