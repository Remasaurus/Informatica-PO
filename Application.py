import time

from numpy import save
from Button import Align, Button, ImgButton, Slider, TextBox, TextButton
from Camera import clamp
from loaders import load_button_events, load_level, load_button_events, load_slider_events
from EventHandler import EventHandler
import json
import pygame
import ctypes

# To change the ugly ass python logo
myappid = 'Anime waifus' # arbitrary string
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
        self.main_size = self.screen.get_size()
        
        with open("./settings.json") as f:
            data = json.load(f)
            self.native = pygame.Vector2(data["native"])
            self.scale = data["scale"]
    
    # TODO: Better name
    def game(self, level):
        """Loads level and enters game loop."""
        event_handler = EventHandler()
        level = load_level(level, event_handler)
        pygame.display.set_mode(self.scale * self.native)
        
        running = True
        def pause(keystate):
            nonlocal running
            if keystate:
                if self.pause():
                    running = False
                    
                
        event_handler.append_key(pygame.K_ESCAPE, pause) 

        while running:
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

        
    def resolution(self):
        with open("./settings.json", "r+") as f:
            data = json.load(f)
            event_handler = EventHandler()
            boxes = [
                TextBox((100, 100), (400, 50), (128, 128, 128), f"{data['native'][0]} x {data['native'][1]}", (0, 0, 0)),
                TextBox((250, 200), (100, 50), (200, 200, 200), f"{data['scale']}", (0, 0, 0)),
                TextBox((100, 300), (400, 50), (128, 128, 128),
                        f"{data['native'][0] * data['scale']} x {data['native'][1] * data['scale']}", (0, 0, 0))
            ]
            
            back_button = TextButton((30, 400), (80, 50),
                    (200, 200, 200), "Back", (0, 0, 0))
            
            sub_button = TextButton((150, 200), (80, 50),
                    (200, 200, 200), "-", (0, 0, 0))
            
            add_button = TextButton((370, 200), (80, 50),
                    (200, 200, 200), "+", (0, 0, 0))
            
            save_button = TextButton((490, 400), (80, 50), (200, 200, 200), "Save", (0, 0, 0))
            
            load_button_events(event_handler, [back_button, sub_button, add_button, save_button])
            
            while 1:
                self.screen.fill("black")
                event_handler.poll()
                for box in boxes:
                    box.draw(self.screen)
                    
                back_button.draw(self.screen)
                if back_button.pressed:
                    return
                
                sub_button.draw(self.screen)
                if sub_button.pressed:
                    data["scale"] = max(1, data["scale"] - 1)
                    boxes[1] = TextBox((250, 200), (100, 50), (200, 200, 200), f"{data['scale']}", (0, 0, 0))
                    boxes[2] = TextBox((100, 300), (400, 50), (128, 128, 128),
                        f"{data['native'][0] * data['scale']} x {data['native'][1] * data['scale']}", (0, 0, 0))
                    
                    sub_button.pressed = False
                
                add_button.draw(self.screen)
                if add_button.pressed:
                    data["scale"] += 1
                    boxes[1] = TextBox((250, 200), (100, 50), (200, 200, 200), f"{data['scale']}", (0, 0, 0))
                    boxes[2] = TextBox((100, 300), (400, 50), (128, 128, 128),
                        f"{data['native'][0] * data['scale']} x {data['native'][1] * data['scale']}", (0, 0, 0))
                    
                    add_button.pressed = False
                    
                save_button.draw(self.screen)
                if save_button.pressed:
                    self.scale = data["scale"]
                    f.seek(0)
                    f.truncate()
                    json.dump(data, f, indent="\t")
                    save_button.pressed = False
                    
                
                pygame.display.flip()
                
                
    
    
    def settings(self):
        pygame.display.set_mode(self.main_size)
        event_handler = EventHandler()
        buttons = [
            TextButton((100, 100), (400, 50),
                    (200, 200, 200), "Resolution", (0, 0, 0)),
            TextButton((150, 200), (300, 50),
                    (200, 200, 200), "Controls", (0, 0, 0)),
            TextButton((200, 300), (200, 50),
                    (200, 200, 200), "Sound", (0, 0, 0)),
            TextButton((30, 400), (80, 50),
                    (200, 200, 200), "Back", (0, 0, 0))
        ]
        
        load_button_events(event_handler, buttons)
        
        
        while True:
            self.screen.fill("black")
            
            
            event_handler.poll()
            for i, button in enumerate(buttons):
                button.draw(self.screen)
                
                if button.pressed:
                    if i == 0:
                        self.resolution()
                    elif i == 1:
                        self.controls()
                    elif i == 2:
                        self.sound()
                    elif i == 3:
                        return
                    
                button.pressed = False
                
                        
            pygame.display.flip()
    
    def controls(self):
        with open("./settings.json", "r+") as f:
            data = json.load(f)
            controls = data["controls"]
            windowX, windowY = pygame.display.get_window_size()
            event_handler = EventHandler()
            # tag Width = 100
            keys = [
                "dash",
                "jump",
                "left",
                "right",
                "up",
                "down",
                "run"
            ]
            tags = [
                TextBox(((windowX - 350) * 0.5, 30), (100, 50), (128, 128, 128), keys[0], (0, 0, 0)),
                TextBox(((windowX - 350) * 0.5, 95), (100, 50), (128, 128, 128), keys[1], (0, 0, 0)),
                TextBox(((windowX - 350) * 0.5, 160), (100, 50), (128, 128, 128), keys[2], (0, 0, 0)),
                TextBox(((windowX - 350) * 0.5, 225), (100, 50), (128, 128, 128), keys[3], (0, 0, 0)),
                TextBox(((windowX - 350) * 0.5, 290), (100, 50), (128, 128, 128), keys[4], (0, 0, 0)),
                TextBox(((windowX - 350) * 0.5, 355), (100, 50), (128, 128, 128), keys[5], (0, 0, 0)),
                TextBox(((windowX - 350) * 0.5, 420), (100, 50), (128, 128, 128), keys[6], (0, 0, 0)),
            ]
            
            buttons = [
                TextButton(((windowX - 350) * 0.5 + 150, 30), (200, 50), (128, 128, 128), controls[keys[0]], (0, 0, 0)),
                TextButton(((windowX - 350) * 0.5 + 150, 95), (200, 50), (128, 128, 128), controls[keys[1]], (0, 0, 0)),
                TextButton(((windowX - 350) * 0.5 + 150, 160), (200, 50), (128, 128, 128), controls[keys[2]], (0, 0, 0)),
                TextButton(((windowX - 350) * 0.5 + 150, 225), (200, 50), (128, 128, 128), controls[keys[3]], (0, 0, 0)),
                TextButton(((windowX - 350) * 0.5 + 150, 290), (200, 50), (128, 128, 128), controls[keys[4]], (0, 0, 0)),
                TextButton(((windowX - 350) * 0.5 + 150, 355), (200, 50), (128, 128, 128), controls[keys[5]], (0, 0, 0)),
                TextButton(((windowX - 350) * 0.5 + 150, 420), (200, 50), (128, 128, 128), controls[keys[6]], (0, 0, 0)),
                
                TextButton((490, 400), (80, 50), (200, 200, 200), "Save", (0, 0, 0)),
                
                TextButton((30, 400), (80, 50),
                    (200, 200, 200), "Back", (0, 0, 0))
            ]
            
            load_button_events(event_handler, buttons)
            selecting = None
            def hook(event):
                nonlocal selecting
                if selecting is not None and event.type == pygame.KEYDOWN:
                    controls[keys[selecting]] = pygame.key.name(event.key)
                    buttons[selecting] = TextButton(((windowX - 350) * 0.5 + 150, 30 + 65 * selecting),
                                                    (200, 50), (128, 128, 128), controls[keys[selecting]], (0, 0, 0))
                    
                    selecting = None
                        
                    
            event_handler.append_hook(hook)

            def mouse(button, state):
                nonlocal selecting
                if button == pygame.BUTTON_LEFT:
                    selecting = None
                
            event_handler.append_mouse(mouse)
            
            while 1:
                self.screen.fill((0, 0, 0))
                event_handler.poll()
                for tag in tags:
                    tag.draw(self.screen)
                    
                for i, button in enumerate(buttons):
                    button.draw(self.screen)
                    
                    if button.pressed:
                        if i == len(buttons) - 1:
                            return
                        elif i == len(buttons) - 2:
                            f.seek(0)
                            f.truncate()
                            json.dump(data, f, indent="\t")
                        else:
                            selecting = i
                            
                        
                        button.pressed = False
                        
                if selecting is not None:
                    s = pygame.Surface((600, 100))
                    s.fill((128, 128, 128))
                    s.set_alpha(200)
                    self.screen.blit(s, (0, 200))
                    
                    
                
                pygame.display.flip()
                

    def play(self):
        # width: 600, height: 500
        event_handler = EventHandler()
        buttons_image = pygame.image.load("img\playButtons.png").convert()
        buttons = [
            ImgButton((40, 150), buttons_image.subsurface((0, 0, 240, 80))),
            ImgButton((40, 300), buttons_image.subsurface((0, 80, 240, 80))),
            ImgButton((320, 150), buttons_image.subsurface((240, 80, 240, 80))),
            ImgButton((320, 300), buttons_image.subsurface((240, 0, 240, 80))),
            TextButton((30, 400), (80, 50),
                    (200, 200, 200), "Back", (0, 0, 0))
        ]
        
        load_button_events(event_handler, buttons)
        
        
        while True:
            self.screen.fill("black")
            
            event_handler.poll()
            for i, button in enumerate(buttons):   
                button.draw(self.screen)
                             
                if button.pressed:
                    if i == 0:
                        self.game("cave")
                    elif i == 1:
                        self.game("cave")
                    elif i == 2:
                        self.game("cave")
                    elif i == 3:
                        self.game("cave")
                    if i == 4:
                        return
                    
                    pygame.display.set_mode(self.main_size)
                    button.pressed = False   
                        
            pygame.display.flip()
        
    def pause(self):
        # load_pause_keyboard(event_handler)
        windowX, windowY = pygame.display.get_window_size()
        buttons = [
            TextButton((0.25 * windowX, 0.3 * windowY), (0.5 * windowX, 0.12 * windowY),
                    (200, 200, 200), "Continue", (0, 0, 0)),
            TextButton((0.35 * windowX, 0.6 * windowY), (0.3 * windowX, 0.12 * windowY),
                    (200, 200, 200), "Settings", (0, 0, 0)),
            TextButton((0.05 * windowX, 0.8 * windowY), (0.16 * windowX, 0.12 * windowY),
                    (200, 200, 200), "Quit", (0, 0, 0))
        ]
        
        event_handler = EventHandler()
        
        load_button_events(event_handler, buttons)
        level = self.screen.copy()
        
        while True:
            self.screen.blit(level, (0, 0))
            overlay = pygame.Surface(self.screen.get_size())
            overlay.set_alpha(128)
            self.screen.blit(overlay, (0, 0))
            
            for i, button in enumerate(buttons):
                    button.draw(self.screen)
                    
            for i, button in enumerate(buttons):
                if button.pressed:
                    if i == 0:
                        return 0
                    elif i == 1:
                        self.settings()
                        pygame.display.set_mode(self.scale * self.native)
                        level = pygame.transform.scale(level, pygame.display.get_window_size())
                        windowX, windowY = pygame.display.get_window_size()
                        buttons = [
                            TextButton((0.25 * windowX, 0.3 * windowY), (0.5 * windowX, 0.12 * windowY),
                                    (200, 200, 200), "Continue", (0, 0, 0)),
                            TextButton((0.35 * windowX, 0.6 * windowY), (0.3 * windowX, 0.12 * windowY),
                                    (200, 200, 200), "Settings", (0, 0, 0)),
                            TextButton((0.05 * windowX, 0.8 * windowY), (0.16 * windowX, 0.12 * windowY),
                                    (200, 200, 200), "Quit", (0, 0, 0))
                        ]
                        event_handler.clear()
                        load_button_events(event_handler, buttons)
                        
                    else:
                        return 1
                        
                    button.pressed = False

            event_handler.poll()

            pygame.display.flip()
    
    
    def sound(self):
        with open("./settings.json", "r+") as f:
            data = json.load(f)
            sound = data["sound"]
            master_volume = Slider((100, 90), (500, 90), 0, 1, sound["master"])
            sfx_volume = Slider((100, 215), (500, 215), 0, 1, sound["sfx"])
            music_volume = Slider((100, 340), (500, 340), 0, 1, sound["music"])
        
            event_handler = EventHandler()
            sliders = [master_volume, sfx_volume, music_volume]
            load_slider_events(event_handler, sliders)
            
            tags = [
                TextBox((100, 50), (1, 1), (255, 255, 255), "Mastervolume", (0, 0, 0), Align.LEFT),
                TextBox((100, 175), (1, 1), (255, 255, 255), "Sfxvolume", (0, 0, 0), Align.LEFT),
                TextBox((100, 300), (1, 1), (255, 255, 255), "background music", (0, 0, 0), Align.LEFT)
            ]
            
            back_button = TextButton((30, 400), (80, 50),
                        (200, 200, 200), "Back", (0, 0, 0))
            
            save_button = TextButton((490, 400), (80, 50), (200, 200, 200), "Save", (0, 0, 0))
            
            load_button_events(event_handler, [back_button, save_button])
            
            
            while 1:
                self.screen.fill((255, 255, 255))
                master_volume.update()
                master_volume.draw(self.screen)
                sfx_volume.update()
                sfx_volume.draw(self.screen)
                music_volume.update()
                music_volume.draw(self.screen)
                
                for tag in tags:
                    tag.draw(self.screen)
                    
                back_button.draw(self.screen)
                if back_button.pressed:
                    return
                
                save_button.draw(self.screen)
                if save_button.pressed:
                    sound["master"] = round(master_volume.current_val, 2)
                    sound["sfx"] = round(sfx_volume.current_val, 2)
                    sound["music"] = round(music_volume.current_val, 2)
                    
                    master_volume.current_val = round(master_volume.current_val, 2)
                    sfx_volume.current_val = round(sfx_volume.current_val, 2)
                    music_volume.current_val = round(music_volume.current_val, 2)
                    
                    
                    f.seek(0)
                    f.truncate()
                    json.dump(data, f, indent="\t")
                    save_button.pressed = False
                
                event_handler.poll()
                
                pygame.display.flip()
    

    def run(self) -> None:
        """Starts the main application loop. After window is closed the program will terminate."""
        event_handler = EventHandler()
        # width: 600, height: 500
        buttons = [
            TextButton((200, 200), (200, 50),
                    (200, 200, 200), "Play", (0, 0, 0)),
            TextButton((200, 300), (200, 50),
                    (200, 200, 200), "Settings", (0, 0, 0)),
            TextButton((200, 400), (200, 50),
                    (200, 200, 200), "Quit", (0, 0, 0))
        ]

        load_button_events(event_handler, buttons)
        
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
                    elif i == 1:                        
                        self.settings()
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
