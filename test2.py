import sys
import pygame
import random


def create_window():
    screen = pygame.display.set_mode((750, 650))
    pygame.display.set_caption("test")
    return screen


class Particle():
    def __init__(self, x, y) -> None:
        self.pos = pygame.Vector2(x, y)
        self.r = random.randint(1, 5)
        self.original_r = self.r

        self.burn_rate = 0.1 * random.randint(1, 4)
        self.glow = 2
        self.layers = 2
        size = 2 * self.r * self.layers * self.layers * self.glow
        self.buffer = pygame.Surface(
            (size, size), pygame.SRCALPHA)

    def update(self):
        self.pos.x += random.randint(-int(self.r), int(self.r))
        self.pos.y -= 7 - self.r
        self.original_r -= self.burn_rate
        self.r = int(self.original_r)

        if self.r <= 0:
            self.r = 1

    def draw(self, surface):
        size = 2 * self.r * self.layers * self.layers * self.glow
        self.buffer = pygame.Surface(
            (size, size), pygame.SRCALPHA)

        for i in range(self.layers, -1, -1):
            alpha = 255 - i * (255 // self.layers - 5)
            if alpha < 0:
                alpha = 0

            radius = self.r * i * i * self.glow

            if self.r == 4 or self.r == 3:
                r, g, b = (255, 0, 0)
            elif self.r == 2:
                r, g, b = (255, 150, 0)
            else:
                r, g, b = (50, 50, 50)

            pygame.draw.circle(self.buffer, (r, g, b, alpha),
                               (self.buffer.get_width()//2, self.buffer.get_height()//2), radius)

        surface.blit(self.buffer, self.buffer.get_rect(center=self.pos))


class ParticleSystem():
    def __init__(self) -> None:
        self.pos = pygame.Vector2(0, 0)
        self.intensity = 100
        self.particles = []

        for _ in range(self.intensity):
            self.particles.append(
                Particle(self.pos.x + random.randint(-7, 7), self.pos.y))

    def update(self):
        for i, particle in enumerate(self.particles):
            particle.update()

            if particle.original_r <= 0:
                self.particles.pop(i)
                self.particles.append(
                    Particle(self.pos.x + random.randint(-7, 7), self.pos.y))

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)


def main():
    screen = create_window()
    fire = ParticleSystem()
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill((0, 0, 0))

        fire.pos = pygame.Vector2(pygame.mouse.get_pos())
        fire.update()
        fire.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
