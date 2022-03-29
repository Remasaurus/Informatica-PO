import pygame
import json
import sys
from Level import Level
from Grid import Grid
from Spritesheet import Spritesheet, create_anim
from components.Dash import Dash
from components.jump import Jump
from components.move import Move
from components.physics import Physics
from components.wallSlide import WallSlide
from components.Follower import Follower
from entities.Player import Player
from entities.Helper import Helper
from layers import BackgroundLayer, EntityLayer, LightingLayer, ParallaxLayer


def load_level(name: str, event_handler) -> Level:
    """Creates level and intializes it with given the json that matches the name."""
    with open(f"./levels/{name}.json", "r") as f:
        data = json.load(f)
        level = Level()
        level.gravity = data["gravity"]
        tile_spritesheet = load_spritesheet(data["tileSheet"])
        charachter_spritesheet = load_spritesheet(data["charachterSheet"])
        collider_grid = Grid(tile_spritesheet.tile_size)
        player = load_player()
        helper = load_helper()
        helper.follow(player)
    
        
        player.pos.x = data["spawnpoint"][0] * tile_spritesheet.tile_size
        player.pos.y = data["spawnpoint"][1] * tile_spritesheet.tile_size

        level.entities.append(player)
        level.entities.append(helper)
        
        load_keyboard(event_handler, player)
        
        for backgroundImg in data["backgroundImages"]:
            level.compositor.layers.append(ParallaxLayer(backgroundImg[0], backgroundImg[1],
                                                         pygame.Vector2(backgroundImg[2]) * tile_spritesheet.tile_size))
        

        for layer in data["layers"]:
            level.compositor.layers.append(
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
        level.compositor.layers.append(entity_layer)
        level.compositor.layers.append(lighting_layer)

        return level


def load_player():
    """Creates player and adds all necessary components."""
    player = Player()
    player.add_component(Move())
    player.add_component(Jump())
    player.add_component(WallSlide())
    player.add_component(Dash())
    player.add_component(Physics())

    return player


def load_helper():
    helper = Helper()
    helper.add_component(Physics())
    helper.add_component(Follower())
    
    return helper
    


# FIXME: Disgusting
def load_menu_keyboard(event_handler, buttons):
    """Loads keyboard that is needed for the menu."""
    def callback(state, button):
        mouse = pygame.mouse.get_pos()
        for button in buttons:
            if button.rect.collidepoint(mouse):
                button.pressed = state

    event_handler.append_mouse(callback)


def load_keyboard(event_handler, player):
    """Adds all keypress functionaly to given player"""
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
        else:
            player.components["Jump"].cancel()

    def dash(keystate):
        if keystate:
            player.components["Dash"].start()

    def run(keystate):
        player.components["Move"].run = keystate

    def quit(keystate):
        sys.exit()

    event_handler.append_key(pygame.K_a, left)
    event_handler.append_key(pygame.K_d, right)
    event_handler.append_key(pygame.K_w, up)
    event_handler.append_key(pygame.K_s, down)
    
    event_handler.append_key(pygame.K_LEFT, left)
    event_handler.append_key(pygame.K_RIGHT, right)
    event_handler.append_key(pygame.K_UP, up)
    event_handler.append_key(pygame.K_DOWN, down)
    
    event_handler.append_key(pygame.K_LSHIFT, run)
    event_handler.append_key(pygame.K_RSHIFT, run)
    
    event_handler.append_key(pygame.K_ESCAPE, quit)
    
    event_handler.append_key(pygame.K_j, dash)
    event_handler.append_key(pygame.K_SPACE, jump)


def load_spritesheet(name: str) -> Spritesheet:
    """Create spritesheets and prerenders all sprites in the json."""
    with open(name, "r") as f:
        data = json.load(f)
        im = pygame.image.load(data["imageURL"])
        s = Spritesheet(im, data["tileSize"])

        if "tiles" in data:
            for tile in data["tiles"]:
                s.define_tile(tile["name"], tile["pos"][0], tile["pos"][1])

        if "images" in data:
            for image in data["images"]:
                s.define(image["name"], image["pos"][0],
                         image["pos"][1], image["width"], image["height"], (image["alpha"] if "alpha" in image else False))

        if "anims" in data:
            for anim in data["anims"]:
                s.define_anim(anim["name"], create_anim(
                    anim["frames"], anim["frameLen"]))

        return s
