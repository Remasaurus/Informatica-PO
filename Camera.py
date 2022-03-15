import pygame


class Camera():
    """Container for the screensize and pos."""

    def __init__(self) -> None:
        self.size = pygame.Vector2(pygame.display.get_surface().get_size())
        self.pos = pygame.Vector2(0, 0)
