import pygame
from components.Component import Component, Sides
from particles.DustParticle import DustParticle

class Jump(Component):
    def __init__(self):
        # Height of the jump
        self.force = 300

        # How long the player can press the jump key for more height
        self.duration = 0.2
        
        
        self.squish_duration = 0.5
        self.squish_points = []
        self.jump_squish_points = [(0.85, 1.3), (1, 1)]
        self.land_squish_points = [(1.15, 0.85), (1, 1)]
        
        

        # How much the x velocity affects the jump
        self.boost = 0.02

        # How long the jump buffers in the air
        self.grace_period = 0.1

        # How long the player can jump while running off the edge
        self.coyote_duration = 0.1

        # helper variables
        self.squish_time = 0
        self.request_time = 0
        self.engage_time = 0
        self.coyote_time = 0

    def start(self):
        self.request_time = self.grace_period

    def cancel(self):
        self.request_time = 0
        self.engage_time = 0

    def obstruct(self, entity, side):
        if side == Sides.BOTTOM:
            self.coyote_time = self.coyote_duration
            
        elif side == Sides.TOP:
            self.cancel()

    def update(self, entity, delta_time, level):
        if self.request_time > 0:
            if self.coyote_time > 0:
                if entity.vel.x < 0:
                    for x in range(int(entity.size.x * 0.5), int(entity.size.x + 1)):
                        level.particle_system.particles.append(
                            DustParticle(entity.pos + (x, entity.size.y)))
                    for y in range(int(entity.size.y * 0.8), int(entity.size.y + 1)):
                        level.particle_system.particles.append(
                            DustParticle(entity.pos + (entity.size.x, y)))
                        
                elif entity.vel.x > 0:
                    for x in range(0, int(entity.size.x * 0.5 + 1)):
                        level.particle_system.particles.append(
                            DustParticle(entity.pos + (x, entity.size.y)))
                    for y in range(int(entity.size.y * 0.8), int(entity.size.y + 1)):

                        level.particle_system.particles.append(
                            DustParticle(entity.pos + (0, y)))
                else:
                    for x in range(0, int(entity.size.x + 1)):
                        level.particle_system.particles.append(
                            DustParticle(entity.pos + (x, entity.size.y)))
                        
                self.engage_time = self.duration
                self.squish_time = self.squish_duration - 0.000000000001
                self.squish_points = self.jump_squish_points
                self.request_time = 0
                self.coyote_time = 0
                entity.vel.y = -(self.force + (abs(entity.vel.x) * self.boost))
                

            self.request_time -= delta_time

        if self.engage_time > 0:
            entity.components["Physics"].gravity_multiplier = 0.3
            self.engage_time -= delta_time
        else:
            entity.components["Physics"].gravity_multiplier = 1
            

        if self.squish_time > 0:
            t = 1 - self.squish_time/self.squish_duration
        
            frame = int(t * (len(self.squish_points) - 1) + 1)
            prev = pygame.Vector2(self.squish_points[frame - 1])
            time_per_frame = self.squish_duration/(len(self.squish_points) - 1)
            t = 1 - (self.squish_time%time_per_frame)/time_per_frame
            
            entity.scale = prev.lerp(self.squish_points[frame], t)
            
            self.squish_time -= delta_time
            
            
            

        self.coyote_time -= delta_time
