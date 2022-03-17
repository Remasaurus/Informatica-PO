import pygame
from Application import create_window


# Idea from lighting
# How I would do it in openGL

AMBIENT = pygame.Color(128, 128, 128)

DIFFUSE = pygame.Color(255, 255, 0)


def main():
    w = create_window()

    lighting = pygame.display.get_surface().copy()
    im = pygame.image.load("img\E6Coa.png").convert_alpha()
    im.fill(DIFFUSE, special_flags=pygame.BLEND_RGB_MULT)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        lighting.fill(AMBIENT)
        mouse_pos = list(map(lambda x: x - 50, pygame.mouse.get_pos()))
        lighting.blit(im, mouse_pos, special_flags=pygame.BLEND_RGBA_ADD)

        w.fill(pygame.Color(32, 32, 32))
        w.blit(lighting, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        # w.blit(lighting, (0, 0))

        pygame.display.flip()


main()
