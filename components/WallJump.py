import math
import pygame
from components.Component import Component, Sides


class WallJump(Component):
    def __init__(self):
        # Height of the jump
        self.force = 555
        self.request_time = 0.03
        self.side = -1

        # How long the player can press the jump key for more height
        self.duration = 0.05
        

        # How much the x velocity affects the jump
        self.boost = 0.02

        # How long the jump buffers in the air
        self.grace_period = 0.1

        # How long the player can jump while running off the edge
        self.coyote_duration = 0.1

        # helper variables
        self.squish_time = 0
        self.request_time = 0
        self.coyote_time = 0
        self.engage_time = 0

    def start(self):
        self.request_time = self.grace_period

    def cancel(self):
        self.request_time = 0

    def obstruct(self, entity, side):
        if side == Sides.RIGHT or side == Sides.LEFT:
            self.side = side
            self.coyote_time = self.coyote_duration
        elif side == Sides.TOP:
            self.cancel()
        elif side == Sides.BOTTOM:
            self.coyote_time = 0
            self.request_time = 0
            

    def update(self, entity, delta_time, level):
        if self.request_time > 0:
            if self.coyote_time > 0:
                self.request_time = 0
                self.coyote_time = 0
                self.engage_time = self.duration
                

            self.request_time -= delta_time
        
        if self.engage_time > 0:
            vec = pygame.Vector2(0, -(self.force + (abs(entity.vel.x) * self.boost)))
            if self.side == Sides.LEFT:
                vec.rotate_ip(40)
            else:
                vec.rotate_ip(-40)
                
            entity.vel = vec
            self.engage_time -= delta_time
            
        self.coyote_time -= delta_time