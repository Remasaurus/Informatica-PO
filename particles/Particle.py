import math
import pygame

# Holds all the base classes.
# Not really happy with current solution
class ParticleEmitter():
    def __init__(self, pos, intensity, duration=math.inf):
        self.particles = []
        self.duration = duration
        self.pos = pygame.Vector2(pos)
        self.intensity = intensity

    def update(self, delta_time):
        for i, particle in sorted(enumerate(self.particles)):
            particle.update(delta_time)

            if not particle.alive:
                self.particles.pop(i)

                self.particles.append(Particle(self.pos.x, self.pos.y))

        self.duration -= delta_time

    def draw(self, surface, camera):
        for particle in self.particles:
            particle.draw(surface, camera)


class Particle():
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)

        self.alive = True

    def draw(self, surface, camera):
        pygame.draw.rect(surface, (255, 28, 100),
                         (self.pos[0], self.pos[1], 10, 10))
        # pygame.draw.rect(surface, self.color, pygame.Rect(
        #     self.pos.x - camera.x, self.pos.y - camera.y, 10, 10))

    def update(self, delta_time):
        pass
