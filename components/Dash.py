from components.Component import Component, Sides
import pygame
    


def lerp(a, b, t):
    return (t * a) + ((1-t) * b)


# class Dash(Component):
#     def __init__(self) -> None:
#         self.dash_duration = 0.1
#         self.dash_length = 100
#         self.dash_vel = 700
#         self.dash_dir = pygame.Vector2(0, 0)
        
#         self.target = (0, 0)
#         self.starting_pos = (0, 0)
        
#         self.dash_time = 0
        
#         self.dir = pygame.Vector2(0, 0)
        
#         self.dashing = False
        
    
#     def start(self, entity):
#         self.dashing = True
            
    
#     def obstruct(self, entity, side):
#         self.dash_time = 0
    
#     def update(self, entity, delta_time, level) -> None:
#         if self.dashing:
#             if self.dir:
#                 self.dash_time = self.dash_duration
#                 self.starting_pos = entity.pos.copy()
                
#                 distance = self.dir.copy()
#                 distance.scale_to_length(self.dash_length)
#                 self.target = self.starting_pos + distance
                
#                 self.dash_dir = self.dir.copy()
#                 self.dash_dir.scale_to_length(self.dash_vel)
                
#                 level.camera.shake(0.05, 2)
                
#                 self.dashing = False
                
#         if self.dash_time > 0:
#             entity.vel = self.dash_dir 
            
#             t = self.dash_time/self.dash_duration
#             entity.pos.x = lerp(self.starting_pos[0], self.target[0], t)
#             entity.pos.y = lerp(self.starting_pos[1], self.target[1], t)
            
#             self.dash_time -= delta_time


class Dash(Component):
    def __init__(self) -> None:
        self.dash_duration = 0.1
        self.dash_vel = 500
        self.dash_dir = pygame.Vector2(0, 0)
        self.dash_time = 0
        
        self.dir = pygame.Vector2(0, 0)
        
        self.dashing = False
        
        self.first_frame = False
        
        self.dashes = 1
        
    
    def start(self):
        if self.dashes > 0:
            if self.dir:                
                self.dashes -= 1
                self.dash_time = self.dash_duration
                
                self.dash_dir = self.dir.copy()
                self.dash_dir.scale_to_length(self.dash_vel)
                            
                self.first_frame = True
            
    
    def obstruct(self, entity, side):
        if side == Sides.BOTTOM:
            self.dashes = 1
        
        self.dash_time = 0
    
    def update(self, entity, delta_time, level) -> None:
        if self.dash_time > 0:            
            if self.first_frame:
                level.camera.shake(0.05, 2)
                self.first_frame = False
                
            entity.vel = self.dash_dir.copy() 
            entity.components["Physics"].gravity_multiplier = 0
            self.dash_time -= delta_time