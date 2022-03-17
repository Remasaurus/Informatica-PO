from math import floor
import pygame


def create_anim(frames, frameLen):
    """Creates animation to pass as argument to spritesheet."""
    def anim(time):
        frameIndex = floor(time/frameLen) % len(frames)
        return frames[frameIndex]

    return anim


class Spritesheet():
    """Prerenders all sprites and then draws them to a surface."""
    def __init__(self, image, tile_size):
        self.image = image
        self.tile_size = tile_size
        self.tiles = dict()
        self.anims = dict()

    def define_tile(self, name, x, y):
        """Prerender tile."""
        self.define(name, x * self.tile_size, y * self.tile_size,
                    self.tile_size, self.tile_size)

    def define_anim(self, name, animation):
        """Load animes. Must define images used first!"""
        self.anims[name] = animation

    def define(self, name, x, y, width, height, alpha=False):
        """Prerender image."""
        def create_buffer(flip):
            if alpha:
                buffer = pygame.Surface((width, height), pygame.SRCALPHA)
            else:
                buffer = pygame.Surface((width, height))

            if not flip:
                buffer.blit(self.image, (0, 0), pygame.Rect(
                    x, y, x + width, y + height))
            else:
                tmp = buffer.copy()
                tmp.blit(self.image, (0, 0), pygame.Rect(
                    x, y, x + width, y + height))

                buffer.blit(pygame.transform.flip(tmp, True, False), (0, 0))

            if alpha:
                return buffer.convert_alpha()
            else:
                return buffer.convert()

        buffers = list(map(create_buffer, [False, True]))

        self.tiles[name] = buffers

    def draw(self, name, surface, x, y, flip=False):
        """Draws images to given surface."""
        surface.blit(self.tiles[name][flip], (x, y))

    def draw_anim(self, name, surface, x, y, time, flip=False):
        """Draws anime to given surface."""
        self.draw(self.anims[name](time), surface, x, y, flip)

    def draw_tile(self, name, surface, x, y, flip=False):
        """Draws tile to given surface."""
        self.draw(name, surface, x * self.tile_size, y * self.tile_size, flip)

    def draw_anim(self, name, surface, x, y, distance, flip=False):
        """Draws animation to given surface."""
        self.draw(self.anims[name](distance), surface, x, y, flip)
