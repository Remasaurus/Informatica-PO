from re import A
import sys
from typing import Iterator
import pygame
from Application import create_window


# Idea for letter by letter text

letter_dict = dict()
letters = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ"
font = pygame.font.SysFont(None, 48)

for l in letters:
    letter_dict[l] = font.render(l, True, (0, 0, 0))

class TextMessage():
    def __init__(self, text) -> None:
        self.text_iter = iter(text)
        self.text = ""
        self.duration = 10
        self.time = self.duration/len(text)
        self.timer = 0
        self.buffer = pygame.Surface((1000, 48))
        self.done = False
        
    def draw(self, surface):
        for i, l in enumerate(self.text):
            surface.blit(letter_dict[l], (i * 48, 0))
            
    
    def changeMessage(self, text):
        self.text = ""
        self.text_iter = iter(text)
        self.time = self.duration/len(text)
        self.timer = 0
        self.done = False
        
        
    def isDone(self):
        return self.done
        
        
    def update(self, dt):
        if self.timer > self.time:
            self.timer -= self.time
            letter = next(self.text_iter, None)
            if letter is not None:
                self.text += letter
            else:
                self.done = True
        
        self.timer += dt
        



def main():
    screen = create_window()
    clock = pygame.time.Clock()

    t = TextMessage("Hello world")

    
    while True:
        dt = clock.tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        
        screen.fill((255, 255, 255))
        
        t.update(dt)
        t.draw(screen)
        
        if t.isDone():
            t.changeMessage("Ooga Booga")
        
        
        pygame.display.flip()
            

if __name__ == "__main__":
    main()