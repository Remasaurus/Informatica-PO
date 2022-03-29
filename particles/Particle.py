import math
import pygame

# Holds all the base classes.
# Not really happy with current solution
class ParticleEmitter():
    def __init__(self, pos, intensity, duration=math.inf):
        self.duration = duration
        self.pos = pygame.Vector2(pos)
        self.time_per_particle = 0.1
        self.time = 0

    def update(self, particle_system, delta_time):        
        while self.time > self.time_per_particle:
            particle_system.particles.append(Particle(self.pos))
            
            self.time -= self.time_per_particle
            
        self.time += delta_time
        self.duration -= delta_time


class Particle():
    def __init__(self, pos):
        self.pos = pygame.math.Vector2(pos)
        self.alive = True

    def draw(self, surface, camera):
        pygame.draw.rect(surface, (255, 28, 100),
                         (self.pos.x - camera.pos.x, self.pos.y - camera.pos.y, 10, 10))
        # pygame.draw.rect(surface, self.color, pygame.Rect(
        #     self.pos.x - camera.x, self.pos.y - camera.y, 10, 10))

    def update(self, delta_time):
        pass
