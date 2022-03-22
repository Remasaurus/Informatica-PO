import time
from Button import Button
from loaders import load_level, load_menu_keyboard
from EventHandler import EventHandler
import json
import pygame

from particles.Fire import FireEmitter


class Application():
    """Application entrypoint."""

    def __init__(self) -> None:
        self.screen = create_window()
        self.clock = pygame.time.Clock()
        self.event_handler = EventHandler()

    def main_menu(self):
        pass
    
    # TODO: Better name
    def game(self, level):
        """Loads level and enters game loop."""
        self.event_handler.clear()

        level = load_level(level, self.event_handler)
        # level.particle_system.emitters.append(FireEmitter((50, 50), 50))

        while True:
            delta_time = self.clock.tick()/1000
            if delta_time > 0.5:
                continue

            start = time.time()

            self.event_handler.poll()

            level.update(delta_time)
            level.draw(self.screen)

            pygame.display.flip()

            # print(f"Frametime: {time.time() - start} sec")

        self.event_handler.clear()

    def run(self) -> None:
        """Starts the main application loop. After window is closed the program will terminate."""

        # self.game("cave")

        buttons = [Button((100, 50), (200, 50),
                          (255, 255, 128), (0, 0, 0), "Cave"),
                   Button((100, 150), (200, 50),
                          (255, 255, 128), (0, 0, 0), "Space")]

        load_menu_keyboard(self.event_handler, buttons)

        while True:
            self.screen.fill((200, 50, 10))

            for i, button in enumerate(buttons):
                button.draw(self.screen)

                if button.pressed:
                    if i == 0:
                        self.game("cave")
                    else:
                        self.game("space")

            self.event_handler.poll()

            pygame.display.flip()


def create_window() -> pygame.Surface:
    """Creates a pygame window and return the window surface."""

    with open("./config.json", "r") as f, open("./tiles.json") as f2:
        data = json.load(f)
        data2 = json.load(f2)

        screen = pygame.display.set_mode(
            (data["window"]["width"] * data2["tileSize"], data["window"]["height"] * data2["tileSize"]), pygame.RESIZABLE)
        pygame.display.set_caption(
            data["window"]["caption"])

        return screen
