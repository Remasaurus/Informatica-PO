import math
import pygame
from components.Animator import Animator
from components.Component import Component, Sides
from particles.FireBall import FireBall
import random
from enum import Enum, auto

class BossMoves(Enum):
    JUMP = auto()
    ATTACK = auto()
    RUN = auto()
    BOUNCE = auto()




class BossAI(Component):
    def __init__(self) -> None:
        # general
        self.current_move = None
        self.moves = list(BossMoves)
        self.duration_between_moves = 0.5
        self.time_between_moves = 0
        self.ready = True
        self.first_frame = False
                
        # jump
        self.jump_force = 400
        self.jump_movement = 100
        
        # bounce
        self.bounce_force = 600
        self.jumps = 0
        self.fall_force = 1000
        
        self.land = False
        self.hold = 0.1
        self.holded = False
        self.holding = 0
        self.delay = 0.2
        self.delaying = 0
        self.bounce_movement = 100
        
        
        # run
        self.fall_first_frame = False
        self.side = 0
        self.falling = False
        self.collide_setback = 100
        self.collide_jump = 200
        self.run_speed = 500
        self.bounces = 0
        self.total_bounces = 2
        
        # attack
        self.time_attack = 0
        self.time_between_fireball = 0.5
        self.timer = 0
        self.duration_attack = 5
        


    def obstruct(self, entity, side):
        if side == Sides.BOTTOM:
            if self.current_move == BossMoves.JUMP:
                self.ready = True
                entity.vel.x = 0
                self.first_jump = True
            elif self.current_move == BossMoves.BOUNCE:
                if not self.land:
                    self.land = True
                    self.holded = False
                    self.jumps += 1
                    self.delaying = self.delay
            
            elif self.falling and not self.fall_first_frame:
                self.fall_first_frame = True
                self.bounces += 1
        
        elif side == Sides.LEFT or side == Sides.RIGHT:
            if self.current_move == BossMoves.RUN:
                self.falling = True
                self.fall_first_frame = True
                self.side = side
                
    def jump(self, entity, delta_time, level):
        if self.first_frame:
            entity.vel.y = -self.jump_force
            entity.vel.x = (random.randint(0, 1) * 2 - 1) * self.jump_movement
        
    def attack(self, entity, delta_time, level):
        if self.first_frame:
            self.time_attack = self.duration_attack
        
        if self.time_attack > 0:
            self.timer += delta_time
            self.time_attack -= delta_time
            if self.timer > self.time_between_fireball:
                self.timer -= self.time_between_fireball
                
                if entity.pos.x < level.entities[0].pos.x:
                    level.particle_system.particles.append(
                        FireBall(entity.pos + (entity.size.x, random.randint(0, entity.size.y)), 1)
                    )
                else:
                    level.particle_system.particles.append(
                        FireBall(entity.pos + (0, random.randint(0, entity.size.y)), -1)
                    )
            
        else:
            self.ready = True
        
    
    def bounce(self, entity, delta_time, level):
        if self.first_frame:
            self.holded = False
            self.land = True
            self.holding = 0
            self.delaying = 0
            self.jumps = 0
            
        if self.delaying > 0:
            self.delaying -= delta_time
            return
        
        if self.jumps >= 3:
            self.ready = True
            return
            
        if self.holding > 0:
            entity.vel.x = 0
            entity.vel.y = 0
            self.holding -= delta_time
            self.holded = True
            return
        elif self.holded:
            entity.vel.y = self.fall_force
            
        if self.land:
            entity.vel.y = -self.bounce_force
            if level.entities[0].pos.x < entity.pos.x:
                entity.vel.x = -self.bounce_movement
            else:
                entity.vel.x = self.bounce_movement
                
            self.land = False
            
        
            
        
        if entity.vel.y > 0 and not self.holded:
            self.holding = self.hold
            
        
    
    def run(self, entity, delta_time, level):
        if self.first_frame:
            self.bounces = 0
            if level.entities[0].pos.x < entity.pos.x:
                entity.vel.x = -self.run_speed
            else:
                entity.vel.x = self.run_speed
        
        elif self.falling:
            self.fall(entity, delta_time, level)
        
        
    def fall(self, entity, delta_time, level):
        if self.fall_first_frame:
            if self.bounces >= self.total_bounces:
                self.ready = True
                entity.vel.x = 0
                return
            
            entity.vel.y = -self.collide_jump
            if self.side == Sides.LEFT:
                entity.vel.x = self.collide_setback / (self.bounces + 1)
            else:
                entity.vel.x = -self.collide_setback / (self.bounces + 1)
                
            self.fall_first_frame = False
            entity.vulnerable = True
            
    
    def update(self, entity, delta_time, level):
        if pygame.Rect(level.camera.pos - (50, 50), level.camera.size + (100, 100)).collidepoint(entity.pos):
            if self.ready:
                self.time_between_moves = self.duration_between_moves
                self.current_move = None
                self.ready = False
                entity.vulnerable = False
                
            elif self.time_between_moves < 0:
                self.current_move = random.choice(self.moves)
                # self.current_move = BossMoves.ATTACK
                self.time_between_moves = 0
                self.first_frame = True
                        
            if self.current_move == BossMoves.JUMP:
                self.jump(entity, delta_time, level)
            elif self.current_move == BossMoves.ATTACK:
                self.attack(entity, delta_time, level)
            elif self.current_move == BossMoves.BOUNCE:
                self.bounce(entity, delta_time, level)
            elif self.current_move == BossMoves.RUN:
                self.run(entity, delta_time, level)
            else:
                self.time_between_moves -= delta_time
            
                
            if entity.vulnerable:
                entity.components["Animator"].add_anim("reswobDown", math.inf, 0, 1)
                if "reswobUp" in entity.components["Animator"].anims:
                    entity.components["Animator"].delete_anim("reswobUp")
                    
                if pygame.Rect(level.entities[0].pos, level.entities[0].size).colliderect(pygame.Rect(entity.pos, entity.size)):
                    entity.hit()
            else:
                entity.components["Animator"].add_anim("reswobUp", math.inf, 0, 1)
                if "reswobDown" in entity.components["Animator"].anims:
                    entity.components["Animator"].delete_anim("reswobDown")
                    
                if pygame.Rect(level.entities[0].pos, level.entities[0].size).colliderect(pygame.Rect(entity.pos, entity.size)):
                    level.entities[0].hit()
                
                
            self.first_frame = False
                                      
                
                
                
    
