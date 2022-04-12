import pygame
import sys


# FIXME: Fix this class in general
class EventHandler():
    """Hides the pygame eventhandler."""
    def __init__(self):
        self.key_callback = dict()
        self.mouse_callbacks = []
        self.hook = None

    def append_key(self, key, key_callback):
        """Add key to eventlistener, calls callback on keyevent."""
        self.key_callback[key] = key_callback

    def append_hook(self, callback):
        self.hook = callback

    def append_mouse(self, callback):
        """Add mouseevent, calls callback on mouseevent."""
        self.mouse_callbacks.append(callback)

    def clear(self):
        """Removes all events from handler."""
        self.key_callback.clear()
        self.mouse_callback = None

    def poll(self):
        """Calls all callbacks if event happened."""
        for event in pygame.event.get():
            if self.hook:
                self.hook(event)
                
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in self.key_callback:
                    self.key_callback[event.key](1)

            elif event.type == pygame.KEYUP:
                if event.key in self.key_callback:
                    self.key_callback[event.key](0)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.mouse_callbacks:
                    for callback in self.mouse_callbacks:
                        callback(1, event.button)

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.mouse_callbacks:
                    for callback in self.mouse_callbacks:
                        callback(0, event.button)
