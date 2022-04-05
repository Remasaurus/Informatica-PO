import pygame
pygame.init()

FONT = pygame.font.SysFont(None, 48)

# FIXME: Fix this class in general
class Button():
    def __init__(self, pos, size, rect_color) -> None:
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.color = rect_color
        self.pressed = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        

class TextButton(Button):
    def __init__(self, pos, size, rect_color, text_color, text) -> None:
        super().__init__(pos, size, rect_color)
        self.text_color = text_color
        self.text_surface = FONT.render(text, True, text_color)
        
    def draw(self, surface):
        super().draw(surface)
        rect = self.text_surface.get_rect()
        center = (self.rect.centerx - rect.width/2,
                  self.rect.centery - rect.height/2)
        surface.blit(self.text_surface, center)