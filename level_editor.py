import json
import pygame
from Camera import Camera
from Grid import Grid
from loaders import load_level
from EventHandler import EventHandler
from Application import create_window
from Button import Button


LAYER = 0
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
        super().__init__(pos, size, (0, 0, 0), (0, 0, 0), "")
        self.img = img
        
    def draw(self, surface, spritesheet):
        spritesheet.draw(self.img, surface, 0, 0)

        
class Selection():
    def __init__(self):
        self.selected = []
        self.start = 0
        self.selecting = 0
        self.size = 0
    
    def update(self, grid: Grid, camera):
        if self.selecting:
            mouse = list(pygame.mouse.get_pos())
            mouse[0] *= SCALE[0]
            mouse[1] *= SCALE[1]
            
            self.size = (mouse + camera.pos) - self.start
            if self.size[0] < 0 or self.size[1] < 0:
                self.size = (0, 0)
                
            x = self.start[0]
            y = self.start[1]
            
            self.selected = grid.get_by_range(x, x + self.size[0], y, y + self.size[1])
    
    def draw(self, surface, camera):
        if self.selecting:
            buffer = pygame.Surface(self.size)
            buffer.fill((255, 255, 255))
            
            buffer.set_alpha(150)
            
            surface.blit(buffer, self.start - camera.pos)

def main():
    global SCALE
    name = input("-> ")
    screen = create_window()
    event_handler = EventHandler()
    level = load_level(name, event_handler)
    level.camera = DraggableCamera()
    buttons = []
    spritesheet = level.compositor.layers[0].spritesheet
    for i, tile in enumerate(spritesheet.tiles.keys()):
        buttons.append(TileButton((0, 0), (spritesheet.tile_size, spritesheet.tile_size), tile))
    
    selection = Selection()
    aspect = level.camera.size.normalize()
    
    changed = [
        
    ]

    actionButtons = [
        Button((0, 0), (30, 50), (0, 0, 0), (255, 255, 255), "Save"),
        Button((0, 0), (30, 50), (0, 0, 0), (255, 255, 255), "Undo")
        
    ]
    
    scroll = [0]
    
    
    def route(keystate, button):
        if button == pygame.BUTTON_LEFT:
            if keystate:
                for i, button in enumerate(actionButtons):
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        if i == 0:
                            with open(f"./levels/{name}.json", "r+") as f:
                                data = json.load(f)
                                for changes in changed:
                                    for tile in changes[0]:
                                        x = level.collider.grid.to_index(tile.x1)
                                        y = level.collider.grid.to_index(tile.y1)
                                        
                                        level.compositor.layers[LAYER].grid.set(x, y, changes[1])
                                    
                                    startX = level.collider.grid.to_index(changes[2][0])
                                    startY = level.collider.grid.to_index(changes[2][1])
                                                                        
                                    endX = level.collider.grid.to_index(changes[3][0] + changes[2][0])
                                    endY = level.collider.grid.to_index(changes[3][1] + changes[2][1])
                                                                    
                                    data["layers"][LAYER]["tiles"].append(
                                        {
                                            "name": changes[1],
                                            "type": "solid",
                                            "range": [
                                                [startX, startY],
                                                [endX + 1, endY + 1]
                                            ]
                                        }
                                    )
                                

                                f.seek(0)
                                f.truncate()
                                json.dump(data, f, indent="\t")
                                changed.clear()
                                
                                    
                        else:
                            changed.pop(-1)
                        
                        return    
                        
                for button in buttons:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        changed.append(
                            [selection.selected, button.img, selection.start, selection.size]
                        )
                        return        
                
            
                selection.start = pygame.Vector2(pygame.mouse.get_pos())
                selection.start[0] *= SCALE[0]
                selection.start[1] *= SCALE[1]
                selection.start += level.camera.pos
            
            selection.selecting = keystate
            
            
        elif button == pygame.BUTTON_RIGHT:
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
        
    event_handler.append_mouse(route)
    event_handler.append_key(pygame.K_ESCAPE, clear)
    
    
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
                spritesheet.draw(changes[1], draw_surface, tile.x1 - level.camera.pos.x, tile.y1 - level.camera.pos.y)

        selection.update(level.collider.grid, level.camera)      
        white_square = pygame.Surface((level.collider.grid.tile_size + 2, level.collider.grid.tile_size + 2))
        white_square.fill((255, 255, 255))
        white_square.set_alpha(150)
            
        for tile in selection.selected:
            draw_surface.blit(white_square, (tile.x1 - 1 - level.camera.pos.x, tile.y1 - 1 - level.camera.pos.y))

        selection.draw(draw_surface, level.camera)
            
                
        pygame.transform.scale(draw_surface, screen.get_size(), screen)
        
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, screen_size[0] * 0.1, screen_size[1]))
        for i, b in enumerate(actionButtons, 1):
            b.rect = pygame.Rect(screen_size[0] - 120 * i , 10, 100, 40)
            b.draw(screen)
            
        for i, button in enumerate(buttons):
            surf = pygame.Surface((spritesheet.tile_size, spritesheet.tile_size))
            button.draw(surf, spritesheet)
            button.rect = pygame.Rect(screen_size[0] * 0.025, screen_size[0] * 0.06 * i + screen_size[0] * 0.025 - scroll[0],
                                       screen_size[0] * 0.05, screen_size[0] * 0.05 )
            screen.blit(pygame.transform.scale(surf, button.rect.size), button.rect.topleft)
        
        pygame.display.flip()
    
    
    





if __name__ == "__main__":
    main()