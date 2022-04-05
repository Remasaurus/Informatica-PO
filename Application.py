import time
from Button import Button, TextButton
from loaders import load_level, load_menu_keyboard, load_pause_keyboard, load_play_keyboard
from EventHandler import EventHandler
import json
import pygame


# // Main menu
# // Play
# // Settings
# // Escape menu


class Application():
    """Application entrypoint."""

    def __init__(self) -> None:
        self.screen = create_window()
        self.clock = pygame.time.Clock()
        self.event_handler = EventHandler()
    
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

            pygame.display.set_caption(f"Frametime: {time.time() - start} sec")
            # print(f"Frametime: {time.time() - start} sec")

        self.event_handler.clear()
    
    
    def settings(self):
        while True:
            pass
    
    
    def play(self):
        load_play_keyboard(self.event_handler)
        while True:
            pass
        
    def pause(self):
        load_pause_keyboard(self.event_handler)
        while True:
            pass
        
    def controls(self):
        pass
    
    
    def sound(self):
        pass
    

    def run(self) -> None:
        """Starts the main application loop. After window is closed the program will terminate."""

        # self.game("cave")
        # width: 600, height: 500
        buttons = [
            TextButton((200, 200), (200, 50),
                    (200, 200, 200), (0, 0, 0), "Play"),
            TextButton((200, 300), (200, 50),
                    (200, 200, 200), (0, 0, 0), "Settings"),
            TextButton((200, 400), (200, 50),
                    (200, 200, 200), (0, 0, 0), "Quit")
        ]

        load_menu_keyboard(self.event_handler, buttons)
        
        background_images = [
            pygame.transform.scale(pygame.image.load("./img/backgroundImg.png").convert(), pygame.display.get_window_size()),
            pygame.transform.scale(pygame.image.load("./img/BrickSpriteSheet.png").convert(), pygame.display.get_window_size()),
            pygame.transform.scale(pygame.image.load("./img/charachters.png").convert(), pygame.display.get_window_size()),
            pygame.transform.scale(pygame.image.load("./img/E6Coa.png").convert(), pygame.display.get_window_size()),
            pygame.transform.scale(pygame.image.load("./img/tiles.png").convert(), pygame.display.get_window_size())
        ]
        
        duration_per_img = 5
        transition_duration = 0.2
        total_time = 0
        overlay = pygame.Surface(pygame.display.get_window_size())

        while True:
            total_time += self.clock.tick()/1000
            relative_time_frame = total_time%duration_per_img    
            
            if relative_time_frame < transition_duration:
                overlay.set_alpha(255 - relative_time_frame/transition_duration * 255)
                
            elif relative_time_frame > duration_per_img - transition_duration:                
                overlay.set_alpha(
                    255 - (duration_per_img - relative_time_frame)/transition_duration * 255
                    )
            else:
                overlay.set_alpha(0)

            imgIndex = int(total_time/duration_per_img)%len(background_images)            
            self.screen.blit(background_images[imgIndex], (0, 0))
            self.screen.blit(overlay, (0, 0))
            
            for i, button in enumerate(buttons):
                button.draw(self.screen)

                if button.pressed:
                    if i == 0:
                        self.game("cave")
                    else:
                        self.settings()

            self.event_handler.poll()

            pygame.display.flip()


def create_window() -> pygame.Surface:
    """Creates a pygame window and return the window surface."""

    with open("./config.json", "r") as f:
        data = json.load(f)

        screen = pygame.display.set_mode(
            (data["window"]["width"], data["window"]["height"]), pygame.RESIZABLE)
        pygame.display.set_caption(
            data["window"]["caption"])
        
        pygame.display.set_icon(pygame.image.load(data["window"]["icon"]))

        return screen
