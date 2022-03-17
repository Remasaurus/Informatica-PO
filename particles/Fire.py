import math
import random
from particles.Particle import ParticleEmitter, Particle
import pygame

# Might change this up later
class FireEmitter(ParticleEmitter):
    def __init__(self, pos, intensity):
        super().__init__(pos, intensity)
        for _ in range(self.intensity):
            self.particles.append(FireParticle(self.pos.x, self.pos.y))

    def update(self, delta_time):
        self.pos = pygame.Vector2(pygame.mouse.get_pos())
        for i, particle in sorted(enumerate(self.particles)):
            particle.update(delta_time)

            if particle.original_r < 0:
                self.particles.pop(i)

                self.particles.append(
                    FireParticle(self.pos.x + random.randint(-7, 7), self.pos.y))

        self.duration -= delta_time


class FireParticle(Particle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.r = random.randint(1, 5)
        self.original_r = self.r

        self.burn_rate = random.randint(2, 8)
        self.glow = 1
        self.layers = 2
        size = 2 * self.r * self.layers * self.layers * self.glow
        self.buffer = pygame.Surface(
            (size, size))

        self.buffer.set_colorkey((0, 0, 0))

    def update(self, delta_time):
        self.pos.x += random.randint(-int(self.r),
                                     int(self.r)) * delta_time * 20
        self.pos.y -= (7 - self.r) * delta_time * 20
        self.original_r -= self.burn_rate * delta_time
        self.r = int(self.original_r)

        if self.r <= 0:
            self.r = 1

    def draw(self, surface, camera):
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
