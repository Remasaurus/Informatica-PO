import pygame
from Camera import Camera


class Compositor():
    """Container around all layers in a scene."""

    def __init__(self):
        self.layers = dict()

    def add_layer(self, layer):
        self.layers[type(layer).__name__] = layer


    def draw(self, surface: pygame.Surface, camera: Camera):
        """Calls every layers' draw method."""
        for layer in self.layers.values():
            layer.draw(surface, camera)
