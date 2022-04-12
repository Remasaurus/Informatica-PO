import pygame
from enum import Enum, auto
from Camera import clamp
pygame.init()

FONT = pygame.font.SysFont(None, 48)


class Align(Enum):
    LEFT = auto()
    CENTRE = auto()


class Box():
    def __init__(self, pos, size, rect_color) -> None:
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.color = rect_color
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        

class Slider():
    SLIDER_HEIGHT = 20
    SLIDER_HEIGHT_SMALL = 5
    SLIDER_SIZE = (10, 20)
    SLIDER_RECT_PADDING = 30
    
    
    def __init__(self, start_pos, end_pos, start_val, end_val, current = 0) -> None:
        self.start_pos = pygame.Vector2(start_pos)
        self.end_pos = pygame.Vector2(end_pos)
        
        self.start_val = start_val
        self.end_val = end_val
        
        self.current_val = current or start_val
        self.dragging = False
        self.bounding_rect = pygame.Rect(self.start_pos - (self.SLIDER_RECT_PADDING, self.SLIDER_HEIGHT + self.SLIDER_RECT_PADDING),
                (self.end_pos - self.start_pos) + (self.SLIDER_RECT_PADDING * 2, (self.SLIDER_HEIGHT + self.SLIDER_RECT_PADDING) * 2))
        
    def draw(self, surface):        
        pygame.draw.line(surface, (0, 0, 0), self.start_pos + (0, self.SLIDER_HEIGHT), self.start_pos - (0, self.SLIDER_HEIGHT), 2)
        pygame.draw.line(surface, (0, 0, 0), self.end_pos + (0, self.SLIDER_HEIGHT), self.end_pos - (0, self.SLIDER_HEIGHT), 2)
        pygame.draw.line(surface, (0, 0, 0), self.start_pos, self.end_pos)
        
        for x in range(int(self.start_pos.x), int(self.end_pos.x), 10):
            pygame.draw.line(surface, (0, 0, 0), (x, self.start_pos.y - self.SLIDER_HEIGHT_SMALL), (x, self.start_pos.y + self.SLIDER_HEIGHT_SMALL))
        
        rect = pygame.Rect((0, 0), self.SLIDER_SIZE)
        rect.center = (self.start_pos.x + (self.end_pos.x - self.start_pos.x) * 
                       ((self.current_val - self.start_val)/(self.end_val - self.start_val)), self.start_pos.y)
        pygame.draw.rect(surface, (0, 0, 0), rect)
        
        
    def update(self):
        if self.dragging:
            mouse = pygame.mouse.get_pos()
            rel_x = clamp(self.start_pos.x, self.end_pos.x, mouse[0]) - self.start_pos.x
            
            t = rel_x/(self.end_pos.x - self.start_pos.x)
            self.current_val = self.start_val + (self.end_val - self.start_val) * t



class TextBox(Box):
    def __init__(self, pos, size, rect_color, text, text_color, align = Align.CENTRE) -> None:
        super().__init__(pos, size, rect_color)
        self.text_surface = FONT.render(text, True, text_color)
        self.align = align
        
    def draw(self, surface):
        super().draw(surface)
        rect = self.text_surface.get_rect()
        if self.align == Align.CENTRE:
            rect.center = self.rect.center
        elif self.align == Align.LEFT:
            rect.left = self.rect.left
            rect.centery = self.rect.centery
        surface.blit(self.text_surface, rect)
    
    
    
    
class Button(Box):
    def __init__(self, pos, size, rect_color) -> None:
        super().__init__(pos, size, rect_color)
        self.pressed = False

        

class ImgButton(Button):
    def __init__(self, pos, image) -> None:
        super().__init__(pos, image.get_size(), (0, 0, 0))
        self.image = image
        
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class TextButton(TextBox):
    def __init__(self, pos, size, rect_color, text, text_color, align = Align.CENTRE) -> None:
        super().__init__(pos, size, rect_color, text, text_color, align)
        self.pressed = False