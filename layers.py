import pygame
from Camera import Camera
from Grid import Grid
from Spritesheet import Spritesheet


class Layer():
    """Base class for all layers. Must overwrite update and draw method."""

    def draw(self, surface: pygame.Surface, camera: Camera) -> None:
        pass


class LightingLayer(Layer):
    def __init__(self, spritesheet, ambient):
        self.spritesheet = spritesheet

        self.im = pygame.image.load("img\E6Coa.png").convert()
        self.ambient = ambient
        self.buffer = pygame.display.get_surface().copy()
        self.lights = []

    def append_light(self, x, y, color, size):
        buffer = pygame.transform.scale(self.im, (size, size))

        buffer.fill(pygame.Color(color), special_flags=pygame.BLEND_RGB_MULT)
        self.lights.append([x * self.spritesheet.tile_size + self.spritesheet.tile_size *
                            0.5 - size * 0.5, y * self.spritesheet.tile_size + self.spritesheet.tile_size * 0.5 - size * 0.5, buffer])

    def draw(self, surface, camera):
        self.buffer.fill(self.ambient)

        for light in self.lights:

            self.buffer.blit(
                light[2], (light[0] - camera.pos.x, light[1] - camera.pos.y), special_flags=pygame.BLEND_RGB_ADD)

        surface.blit(self.buffer, (0, 0), special_flags=pygame.BLEND_RGB_MULT)

        # self.buffer.fill(self.ambient)
        # surface.blit(self.buffer, (0, 0), special_flags=pygame.BLEND_RGB_MULT)

        # for light in self.lights:

        #     surface.blit(
        #         light[2], (light[0] - camera.pos.x, light[1] - camera.pos.y), special_flags=pygame.BLEND_RGB_ADD)


class EntityLayer(Layer):
    """Layer class that contains all entities"""

    def __init__(self, spritesheet: Spritesheet, entities: list) -> None:
        self.spritesheet = spritesheet
        self.entities = entities

    def draw(self, surface: pygame.Surface, camera: Camera) -> None:
        """Draws all entities relative to camera"""
        for entity in self.entities:
            entity.draw(surface, camera, self.spritesheet)


class BackgroundLayer(Layer):
    """Layer class that contains all tiles in a singular layer."""

    def __init__(self, spritesheet: Spritesheet, layer: dict) -> None:
        self.spritesheet = spritesheet

        self.grid = Grid(self.spritesheet.tile_size)

        for tile in layer["tiles"]:
            [start, end] = tile["range"]
            for x in range(start[0], end[0]):
                for y in range(start[1], end[1]):
                    self.grid.set(x, y, tile["name"])

        window_size = list(pygame.display.get_surface().get_size())
        window_size[0] += self.spritesheet.tile_size
        window_size[1] += self.spritesheet.tile_size

        self.buffer = pygame.Surface(window_size)
        self.prev_startX = -1
        self.prev_startY = -1

    def redraw(self, camera):
        startX = self.grid.to_index(camera.pos.x)
        startY = self.grid.to_index(camera.pos.y)

        if startX == self.prev_startX and startY == self.prev_startY:
            return

        self.prev_startX = startX
        self.prev_startY = startY

        endX = startX + self.grid.to_index(camera.size.x)
        endY = startY + self.grid.to_index(camera.size.y)

        # for x in range(startX, endX + 1):
        #     col = self.grid.get_col(x)
        #     for y, name in enumerate(col):
        #         if name:
        #             self.spritesheet.draw_tile(
        #                 name, self.buffer, x - startX, y)

        for x in range(startX, endX + 1):
            for y in range(startY, endY + 1):
                name = self.grid.get(x, y)
                if name:
                    self.spritesheet.draw_tile(
                        name, self.buffer, x - startX, y - startY)

    def draw(self, surface: pygame.Surface, camera: Camera) -> None:
        """Draws all tiles that fit in camera on the given surface."""
        self.redraw(camera)
        surface.blit(self.buffer, (-(camera.pos.x %
                                     self.spritesheet.tile_size), -(camera.pos.y % self.spritesheet.tile_size)))
