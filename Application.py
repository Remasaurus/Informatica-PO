import time
from Button import Button, TextButton
from loaders import load_level, load_menu_keyboard, load_pause_keyboard, load_play_keyboard
from EventHandler import EventHandler
import json
import pygame
import ctypes

# To change the ugly ass python logo
myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


# // Main menu
# // Play
# // Settings
# // Escape menu

class Application():
    """Application entrypoint."""

    def __init__(self) -> None:
        self.screen = create_window()
        self.clock = pygame.time.Clock()
    
    # TODO: Better name
    def game(self, level):
        """Loads level and enters game loop."""
        event_handler = EventHandler()
        level = load_level(level, event_handler)
        def pause(keystate):
            if keystate:
                self.pause()
                
        event_handler.append_key(pygame.K_ESCAPE, pause) 
        # level.particle_system.emitters.append(FireEmitter((50, 50), 50))

        while True:
            delta_time = self.clock.tick()/1000
            if delta_time > 0.5:
                continue

            start = time.time()

            event_handler.poll()

            level.update(delta_time)
            level.draw(self.screen)

            pygame.display.flip()

            pygame.display.set_caption(f"Frametime: {time.time() - start} sec")
            # print(f"Frametime: {time.time() - start} sec")

        
    
    
    def settings(self):
        event_handler = EventHandler()
        buttons = [
            TextButton((150, 150), (300, 50),
                    (200, 200, 200), (0, 0, 0), "Controls"),
            TextButton((200, 300), (200, 50),
                    (200, 200, 200), (0, 0, 0), "Sound"),
            TextButton((30, 400), (80, 50),
                    (200, 200, 200), (0, 0, 0), "Back")
        ]
        
        load_menu_keyboard(event_handler, buttons)
        
        
        while True:
            self.screen.fill("black")
            
            
            event_handler.poll()
            for i, button in enumerate(buttons):
                button.draw(self.screen)
                
                if button.pressed:
                    if i == 2:
                        return
                    
                button.pressed = False
                
                        
            pygame.display.flip()
    
    
    def play(self):
        # width: 600, height: 500
        event_handler = EventHandler()
        buttons = [
            TextButton((75, 150), (200, 50),
                    (200, 200, 200), (0, 0, 0), "Cave"),
            TextButton((75, 300), (200, 50),
                    (200, 200, 200), (0, 0, 0), "Land"),
            TextButton((325, 150), (200, 50),
                    (200, 200, 200), (0, 0, 0), "Sky"),
            TextButton((325, 300), (200, 50),
                    (200, 200, 200), (0, 0, 0), "Moon"),
            TextButton((30, 400), (80, 50),
                    (200, 200, 200), (0, 0, 0), "Back")
        ]
        
        load_menu_keyboard(event_handler, buttons)
        
        
        while True:
            self.screen.fill("black")
            
            
            event_handler.poll()
            for i, button in enumerate(buttons):
                button.draw(self.screen)
                
                if button.pressed:
                    if i == 4:
                        return
                    elif i == 0:
                        self.game("cave")
                        
                button.pressed = False
                        
            pygame.display.flip()
        
    def pause(self):
        # load_pause_keyboard(event_handler)
        buttons = [
            TextButton((150, 150), (300, 50),
                    (200, 200, 200), (0, 0, 0), "Continue"),
            TextButton((200, 300), (200, 50),
                    (200, 200, 200), (0, 0, 0), "Settings"),
            TextButton((30, 400), (80, 50),
                    (200, 200, 200), (0, 0, 0), "Quit")
        ]
        
        event_handler = EventHandler()
        
        load_menu_keyboard(event_handler, buttons)
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        for i, button in enumerate(buttons):
                button.draw(self.screen)
        
        while True:
            for i, button in enumerate(buttons):
                if button.pressed:
                    if i == 0:
                        return
                    elif i == 1:
                        
                        self.settings()
                        load_menu_keyboard(event_handler, buttons)
                    else:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
                        
                    button.pressed = False

            event_handler.poll()

            pygame.display.flip()
            
            
        
    def controls(self):
        pass
    
    
    def sound(self):
        pass
    

    def run(self) -> None:
        """Starts the main application loop. After window is closed the program will terminate."""
        event_handler = EventHandler()
        # width: 600, height: 500
        buttons = [
            TextButton((200, 200), (200, 50),
                    (200, 200, 200), (0, 0, 0), "Play"),
            TextButton((200, 300), (200, 50),
                    (200, 200, 200), (0, 0, 0), "Settings"),
            TextButton((200, 400), (200, 50),
                    (200, 200, 200), (0, 0, 0), "Quit")
        ]

        load_menu_keyboard(event_handler, buttons)
        
        background_images = [
            pygame.transform.scale(pygame.image.load("./img/backgroundImg.png").convert(), pygame.display.get_window_size()),
            pygame.transform.scale(pygame.image.load("./img/icon.jpg").convert(), pygame.display.get_window_size()),
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
                        
                        self.play()
                        load_menu_keyboard(event_handler, buttons)
                    elif i == 1:
                        
                        self.settings()
                        load_menu_keyboard(event_handler, buttons)
                    else:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
                        
                    button.pressed = False

            event_handler.poll()

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
        if "cursor" in data:
            pygame.mouse.set_cursor(pygame.Cursor(data["cursor"]["hotspot"], pygame.image.load(data["cursor"]["img"])))
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
            

        return screen
