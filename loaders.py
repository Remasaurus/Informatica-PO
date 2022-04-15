import pygame
import json
import sys
from Level import Level
from Grid import Grid
from Spritesheet import Spritesheet, create_anim
from entities.Boss import Boss
from entities.Player import Player
from entities.Helper import Helper
from layers import BackgroundLayer, EntityLayer, LightingLayer, ParallaxLayer


def load_level(name: str, event_handler) -> Level:
    """Creates level and intializes it with given the json that matches the name."""
    with open(f"./levels/{name}.json", "r") as f, open("./settings.json", "r") as f2:
        data = json.load(f)
        settings = json.load(f2)
        level = Level()
        level.gravity = data["gravity"]
        tile_spritesheet = load_spritesheet(data["tileSheet"])
        charachter_spritesheet = load_spritesheet(data["charachterSheet"])
        collider_grid = Grid(tile_spritesheet.tile_size)
        player = Player()
        helper = Helper()
        helper.follow(player)
        
        level.camera.size.update(settings["native"])
        # level.camera.minX = data["camera"][0][0]
        # level.camera.minY = data["camera"][0][1]
        # level.camera.maxX = data["camera"][1][0]
        # level.camera.maxY = data["camera"][1][1]
    
        
        player.pos.x = data["spawnpoint"][0] * tile_spritesheet.tile_size
        player.pos.y = data["spawnpoint"][1] * tile_spritesheet.tile_size
        level.entities.append(player)
        level.entities.append(helper)
        if "boss" in data:
            boss = Boss()
            
            boss.pos.x = data["boss"][0] * tile_spritesheet.tile_size
            boss.pos.y = data["boss"][1] * tile_spritesheet.tile_size
        
            level.entities.append(boss)
        
        load_keyboard(event_handler, player)
        
        for backgroundImg in data["backgroundImages"]:
            level.compositor.add_layer(ParallaxLayer(backgroundImg[0], backgroundImg[1],
                                                         pygame.Vector2(backgroundImg[2]) * tile_spritesheet.tile_size))
        

        for layer in data["layers"]:
            level.compositor.add_layer(
                BackgroundLayer(tile_spritesheet, layer))

            for tile in layer["tiles"]:
                [start, end] = tile["range"]
                for x in range(start[0], end[0]):
                    for y in range(start[1], end[1]):
                        collider_grid.set(x, y, tile["type"])

        level.collider.grid = collider_grid

        lighting_layer = LightingLayer(tile_spritesheet, data["ambient"])
        for light in data["lights"]:
            lighting_layer.append_light(
                light["pos"][0], light["pos"][1], light["color"], light["size"])

        entity_layer = EntityLayer(charachter_spritesheet, level.entities)
        level.compositor.add_layer(entity_layer)
        level.compositor.add_layer(lighting_layer)
        
        
        

        return level
    
def load_slider_events(event_handler, sliders):
    def callback(state, button):
        if button == pygame.BUTTON_LEFT:
            mouse = pygame.mouse.get_pos()
            if state:
                for slider in sliders:
                    if slider.bounding_rect.collidepoint(mouse):
                        slider.dragging = True
            else:
                for slider in sliders:
                    slider.dragging = False
            
    event_handler.append_mouse(callback)


def load_button_events(event_handler, buttons):
    """Loads keyboard that is needed for the menu."""
    def callback(state, button):
        if state and button == pygame.BUTTON_LEFT:
            mouse = pygame.mouse.get_pos()
            for button in buttons:
                if button.rect.collidepoint(mouse):
                    button.pressed = state

    event_handler.append_mouse(callback)



def load_keyboard(event_handler, player):
    """Adds all keypress functionaly to given player"""
    with open("./settings.json", "r") as f:
        controls = json.load(f)["controls"]
        def left(keystate):
            if keystate:
                player.components["Move"].dir -= 1
                player.components["Dash"].dir.x -= 1
            else:
                player.components["Move"].dir += 1
                player.components["Dash"].dir.x += 1
                

        def right(keystate):
            if keystate:
                player.components["Move"].dir += 1
                player.components["Dash"].dir.x += 1
            else:
                player.components["Move"].dir -= 1
                player.components["Dash"].dir.x -= 1
                
        def up(keystate):
            if keystate:
                player.components["Dash"].dir.y -= 1
            else:
                player.components["Dash"].dir.y += 1
                

        def down(keystate):
            if keystate:
                player.components["Dash"].dir.y += 1
            else:
                player.components["Dash"].dir.y -= 1

        def jump(keystate):
            if keystate:
                player.components["Jump"].start()
                player.components["WallJump"].start()
            else:
                player.components["Jump"].cancel()
                player.components["WallJump"].cancel()


        def dash(keystate):
            if keystate:
                player.components["Dash"].start()

        def run(keystate):
            player.components["Move"].run = keystate

        def quit(keystate):
            sys.exit()

        event_handler.append_key(pygame.key.key_code(controls["left"]), left)
        event_handler.append_key(pygame.key.key_code(controls["right"]), right)
        event_handler.append_key(pygame.key.key_code(controls["up"]), up)
        event_handler.append_key(pygame.key.key_code(controls["down"]), down)
        
        event_handler.append_key(pygame.key.key_code(controls["run"]), run)
        
        event_handler.append_key(pygame.key.key_code(controls["dash"]), dash)
        event_handler.append_key(pygame.key.key_code(controls["jump"]), jump)
    


def load_spritesheet(name: str) -> Spritesheet:
    """Create spritesheets and prerenders all sprites in the json."""
    with open(name, "r") as f:
        data = json.load(f)
        im = pygame.image.load(data["imageURL"])
        s = Spritesheet(im, data["tileSize"])

        if "tiles" in data:
            for tile in data["tiles"]:
                s.define_tile(tile["name"], tile["pos"][0], tile["pos"][1], (tile["alpha"] if "alpha" in tile else False))

        if "images" in data:
            for image in data["images"]:
                s.define(image["name"], image["pos"][0],
                         image["pos"][1], image["width"], image["height"], (image["alpha"] if "alpha" in image else False))

        if "anims" in data:
            for anim in data["anims"]:
                s.define_anim(anim["name"], create_anim(
                    anim["frames"], anim["frameLen"]))

        return s
