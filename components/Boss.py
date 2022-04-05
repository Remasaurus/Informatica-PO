from locale import currency
import pygame
from components.Component import Component, Sides
import random
from enum import Enum, auto

class BossMoves(Enum):
    JUMP = auto()
    ATTACK = auto()




class BossAI(Component):
    def __init__(self) -> None:
        self.current_move = None
        self.moves = list(BossMoves)
        self.jump_force = 400
        self.duration_between_moves = 2
        self.time_between_moves = 0
        
        self.ready = True
        
        
        self.first_jump = False
                
    def obstruct(self, entity, side):
        if side == Sides.BOTTOM:
            if self.current_move == BossMoves.JUMP:
                self.ready = True
                entity.vel.x = 0
                self.first_jump = True
                
    def jump(self, entity, delta_time, level):
        if self.first_jump:
            entity.vel.y = -self.jump_force
            entity.vel.x = (random.randint(0, 1) * 2 - 1) * 100
            self.first_jump = False
        
    def attack(self, entity, delta_time, level):
        self.ready = True
        
    
    def update(self, entity, delta_time, level):
        if pygame.Rect(level.camera.pos - (50, 50), level.camera.size + (100, 100)).collidepoint(entity.pos):
            if self.ready:
                self.time_between_moves = self.duration_between_moves
                self.current_move = None
                self.ready = False
                
            elif self.time_between_moves < 0:
                # self.current_move = random.choice(self.moves)
                self.current_move = BossMoves.JUMP
                self.time_between_moves = 0
                        
            if self.current_move == BossMoves.JUMP:
                self.jump(entity, delta_time, level)
            elif self.current_move == BossMoves.ATTACK:
                self.attack(entity, delta_time, level)
            else:
                self.time_between_moves -= delta_time
                                      
                
                
                
    
