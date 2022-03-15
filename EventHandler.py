import pygame
import sys


class EventHandler():
    def __init__(self):
        self.key_callback = dict()
        self.mouse_callback = None

    def append_key(self, key, key_callback):
        self.key_callback[key] = key_callback

    def append_mouse(self, callback):
        self.mouse_callback = callback

    def clear(self):
        self.key_callback.clear()
        self.mouse_callback = None

    def poll(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in self.key_callback:
                    self.key_callback[event.key](1)

            elif event.type == pygame.KEYUP:
                if event.key in self.key_callback:
                    self.key_callback[event.key](0)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.mouse_callback:
                    self.mouse_callback(1)

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.mouse_callback:
                    self.mouse_callback(0)
