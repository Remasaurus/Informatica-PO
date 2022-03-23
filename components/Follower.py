from components.Component import Component
import pygame

class Follower(Component):
    def __init__(self):
        self.max_distance = 200
        
        self.max_vel = 500
        self.vel = 3
        
        self.target_offset = pygame.Vector2(0, -64)
        
    
    def update(self, entity, delta_time, level):
        self.target_offset = pygame.Vector2(entity.following.vel.x * -0.1, -64)
        
        target = entity.following.pos + self.target_offset
        vel = (target - entity.pos) * self.vel
        if vel.magnitude() > self.max_vel:
            vel.scale_to_length(self.max_vel)
        
        entity.vel = vel.copy()
        
        
        
        
        
        
        
        