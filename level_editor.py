import json
import pygame
from Camera import Camera
from Grid import Grid
from layers import BackgroundLayer
from loaders import load_level
from EventHandler import EventHandler
from Application import create_window
from Button import Button, TextButton

FONT = pygame.font.SysFont(None, 48)
layer = 0
SCALE = (0, 0)


class DraggableCamera(Camera):
    def __init__(self) -> None:
        super().__init__()
        self.dragging = False
        self.offset = pygame.Vector2(0, 0)

    def update(self):
        if self.dragging:
            mouse = pygame.Vector2(pygame.mouse.get_pos())
            mouse[0] *= SCALE[0]
            mouse[1] *= SCALE[1]

            self.pos += self.offset - mouse
            self.offset = mouse

    def drag(self, keystate):
        self.dragging = keystate
        mouse = pygame.Vector2(pygame.mouse.get_pos())
        mouse[0] *= SCALE[0]
        mouse[1] *= SCALE[1]
        self.offset = mouse


class TileButton(Button):
    def __init__(self, pos, size, img) -> None:
        super().__init__(pos, size, (0, 0, 0))
        self.img = img

    def draw(self, surface, spritesheet):
        spritesheet.draw(self.img, surface, 0, 0)


class DeleteButton(Button):
    def __init__(self, pos, size) -> None:
        super().__init__(pos, size, (0, 0, 0))
        self.img = "None"
        self.buffer = pygame.Surface(size)

    def draw(self, surface, spritesheet):
        surface.blit(self.buffer, (0, 0))


class Box(Button):
    def __init__(self, pos, size):
        super().__init__(pos, size, (255, 222, 173))


class TextBox(Box):
    def __init__(self, pos, size) -> None:
        super().__init__(pos, size)
        self.typing = False
        self.text = ""
        
    def draw(self, surface):
        super().draw(surface)
        self.text_surface = FONT.render(self.text, True, (0, 0, 0))
        rect = self.text_surface.get_rect()
        center = (self.rect.centerx - rect.width/2,
                  self.rect.centery - rect.height/2)
        surface.blit(self.text_surface, center)


class Selection():
    def __init__(self):
        self.selected = []
        self.start = 0
        self.selecting = 0
        self.size = 0
        
        self.rect = pygame.Rect(0, 0, 5, 5)

    def update(self, grid: Grid, camera):
        if self.selecting:
            mouse = list(pygame.mouse.get_pos())
            mouse[0] *= SCALE[0]
            mouse[1] *= SCALE[1]

            self.size = (mouse + camera.pos) - self.start
            if self.size[0] < 0 or self.size[1] < 0:
                self.rect.x = self.start[0] + self.size[0]
                self.rect.y = self.start[1] + self.size[1]
                
                
    
            self.rect.x = min(self.start[0], self.start[0] + self.size[0])
            self.rect.y = min(self.start[1], self.start[1] + self.size[1])
        
                
            self.rect.width = abs(self.size[0])
            self.rect.height = abs(self.size[1])

            self.selected = grid.get_by_range(
                self.rect.left, self.rect.right, self.rect.top, self.rect.bottom)

    def draw(self, surface, camera):
        if self.selecting:
            buffer = pygame.Surface(self.rect.size)
            buffer.fill((255, 255, 255))

            buffer.set_alpha(150)

            surface.blit(buffer, self.rect.topleft - camera.pos)


def check_overlap(tiles):
    for i, tile in reversed(list(enumerate(tiles[:-1]))):
        ranges = set()
        for x in range(tile["range"][0][0], tile["range"][1][0]):
            for y in range(tile["range"][0][1], tile["range"][1][1]):
                ranges.add((x, y))
        
        for other in tiles[i + 1:]:
            for x in range(other["range"][0][0], other["range"][1][0]):
                for y in range(other["range"][0][1], other["range"][1][1]):
                    ranges.discard((x, y))
            

        if not ranges:                     
            print("pop")
            print(tile)
            print(i)   
            tiles.pop(i)
                        
            


def main():
    global SCALE
    name = input("-> ")
    screen = create_window()
    event_handler = EventHandler()
    level = load_level(name, event_handler)
    level.camera = DraggableCamera()
    buttons = []

    spritesheet = level.compositor.layers["BackgroundLayer"].spritesheet

    buttons.append(DeleteButton((0, 0), (spritesheet.tile_size, spritesheet.tile_size)))
    for i, tile in enumerate(spritesheet.tiles.keys()):
        buttons.append(TileButton(
            (0, 0), (spritesheet.tile_size, spritesheet.tile_size), tile))

    selection = Selection()
    aspect = level.camera.size.normalize()

    changed = [

    ]

    actionButtons = [
        TextButton((0, 0), (30, 50), (255, 222, 173), "Save", (0, 0, 0)),
        TextButton((0, 0), (30, 50), (255, 222, 173), "Undo", (0, 0, 0))

    ]

    scroll = [0]
    
    typeBox = TextBox((0, 0), (100, 40))
    layerBox = TextBox((0, 0), (40, 40))
    layerBox.text = f"{layer}"
    
    def hook(event):
        if event.type == pygame.KEYDOWN:
            if typeBox.typing:
                if event.key == pygame.K_BACKSPACE:
                    typeBox.text = typeBox.text[:-1]
                else:
                    typeBox.text += event.unicode
        

    def route(keystate, button):
        global layer
        if button == pygame.BUTTON_LEFT:
            if typeBox.rect.collidepoint(pygame.mouse.get_pos()):
                typeBox.typing = True
                return

            typeBox.typing = False
            
            if keystate:
                if layerBox.rect.collidepoint(pygame.mouse.get_pos()):
                    layer += 1
                    layerBox.text = f"{layer}"
                    return
                
                for i, button in enumerate(actionButtons):
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        if i == 0:
                            with open(f"./levels/{name}.json", "r+") as f:
                                data = json.load(f)
                                if len(data["layers"]) <= layer:
                                    for i in range(layer - len(data["layers"] + 1)):
                                        data.append([])
                                    
                                for changes in changed:
                                    for tile in changes[0]:
                                        x = level.collider.grid.to_index(
                                            tile.x1)
                                        y = level.collider.grid.to_index(
                                            tile.y1)

                                        if changes[1] == "None":
                                            level.compositor.layers["BackgroundLayer"].grid.set(
                                                x, y, None)
                                        else:
                                            level.compositor.layers["BackgroundLayer"].grid.set(
                                                x, y, changes[1])

                                    startX = level.collider.grid.to_index(
                                        changes[2][0])
                                    startY = level.collider.grid.to_index(
                                        changes[2][1])

                                    endX = level.collider.grid.to_index(
                                        changes[3][0] + changes[2][0])
                                    endY = level.collider.grid.to_index(
                                        changes[3][1] + changes[2][1])

                                    data["layers"][layer]["tiles"].append(
                                        {
                                            "name": changes[1],
                                            "type": changes[4],
                                            "range": [
                                                [startX, startY],
                                                [endX + 1, endY + 1]
                                            ]
                                        }
                                    )

                                check_overlap(data["layers"][layer]["tiles"])

                                f.seek(0)
                                f.truncate()
                                json.dump(data, f, indent="\t")
                                changed.clear()

                        else:
                            if changed:
                                changed.pop(-1)

                        return

                for button in buttons:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        changed.append(
                            [selection.selected, button.img,
                                selection.rect.topleft, selection.rect.size, typeBox.text]
                        )
                        return

                selection.start = pygame.Vector2(pygame.mouse.get_pos())
                selection.start[0] *= SCALE[0]
                selection.start[1] *= SCALE[1]
                selection.start += level.camera.pos

            selection.selecting = keystate

        elif button == pygame.BUTTON_RIGHT:
            if keystate:            
                if layerBox.rect.collidepoint(pygame.mouse.get_pos()):
                    layer -= 1
                    layerBox.text = f"{layer}"
                    return
                
            level.camera.drag(keystate)
            
        elif button == pygame.BUTTON_WHEELDOWN:
            if pygame.Rect(0, 0, screen_size[0] * 0.1, screen_size[1]).collidepoint(pygame.mouse.get_pos()):
                scroll[0] += 3
            else:
                level.camera.size += aspect * 5
        elif button == pygame.BUTTON_WHEELUP:
            if pygame.Rect(0, 0, screen_size[0] * 0.1, screen_size[1]).collidepoint(pygame.mouse.get_pos()):
                scroll[0] -= 3
            else:
                level.camera.size -= aspect * 5

    def clear(keystate):
        selection.selected = []
        
    def print_rel_pos(keystate):
        if keystate:
            m = list(pygame.mouse.get_pos())
            m[0] *= SCALE[0]
            m[1] *= SCALE[1]
            
            print(m + level.camera.pos)

    event_handler.append_mouse(route)
    event_handler.append_key(pygame.K_ESCAPE, clear)
    event_handler.append_key(pygame.K_TAB, print_rel_pos)
    
    event_handler.append_hook(hook)
    

    while True:
        draw_surface = pygame.Surface(level.camera.size)
        screen_size = screen.get_size()
        draw_size = draw_surface.get_size()

        SCALE = (draw_size[0]/screen_size[0], draw_size[1]/screen_size[1])

        event_handler.poll()

        level.camera.update()
        level.draw(draw_surface)

        for changes in changed:
            for tile in changes[0]:
                if changes[1] == "None":
                    draw_surface.blit(pygame.Surface((spritesheet.tile_size, spritesheet.tile_size)),
                                      (tile.x1 - level.camera.pos.x, tile.y1 - level.camera.pos.y))
                else: 
                    spritesheet.draw(
                        changes[1], draw_surface, tile.x1 - level.camera.pos.x, tile.y1 - level.camera.pos.y)

        selection.update(level.collider.grid, level.camera)
        white_square = pygame.Surface(
            (level.collider.grid.tile_size + 2, level.collider.grid.tile_size + 2))
        white_square.fill((255, 255, 255))
        white_square.set_alpha(150)

        for tile in selection.selected:
            draw_surface.blit(
                white_square, (tile.x1 - 1 - level.camera.pos.x, tile.y1 - 1 - level.camera.pos.y))

        selection.draw(draw_surface, level.camera)

        pygame.transform.scale(draw_surface, screen.get_size(), screen)

        pygame.draw.rect(screen, (255, 222, 173), pygame.Rect(
            0, 0, screen_size[0] * 0.1, screen_size[1]))
        
        
        typeBox.rect.x = screen_size[0] * 0.15
        typeBox.rect.y = 10
        typeBox.rect.width = screen_size[0] * 0.35
        
        
        typeBox.draw(screen)
        
        layerBox.rect.x = screen_size[0] - 60
        layerBox.rect.y = 60
        
        layerBox.draw(screen)
        
        
        for i, b in enumerate(actionButtons, 1):
            b.rect = pygame.Rect(screen_size[0] - 120 * i, 10, 100, 40)
            b.draw(screen)

        for i, button in enumerate(buttons):
            surf = pygame.Surface(
                (spritesheet.tile_size, spritesheet.tile_size))
            button.draw(surf, spritesheet)
            button.rect = pygame.Rect(screen_size[0] * 0.025, screen_size[0] * 0.06 * i + screen_size[0] * 0.025 - scroll[0],
                                      screen_size[0] * 0.05, screen_size[0] * 0.05)
            screen.blit(pygame.transform.scale(
                surf, button.rect.size), button.rect.topleft)

        pygame.display.flip()


if __name__ == "__main__":
    main()
