from components.Component import Component
from enum import Enum, auto


class DashDirection(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    


def lerp(a, b, t):
    return (t * a) + ((1-t) * b)


class Dash(Component):
    def __init__(self) -> None:
        self.dash_duration = 0.1
        self.dash_length = 100
        
        self.target = (0, 0)
        self.starting_pos = (0, 0)
        
        self.dash_time = 0
        
    
    def start(self, entity):
        self.dash_time = self.dash_duration
        self.starting_pos = entity.pos.copy()
        self.target = self.starting_pos + (self.dash_length, -self.dash_length)
    
    def obstruct(self, entity, side):
        pass
        # self.dash_time = 0
    
        
    def update(self, entity, delta_time, level) -> None:
        if self.dash_time > 0:
            t = self.dash_time/self.dash_duration
            entity.pos.x = lerp(self.starting_pos[0], self.target[0], t)
            entity.pos.y = lerp(self.starting_pos[1], self.target[1], t)
            entity.vel.x = 0
            entity.vel.y = 0
                
            
            self.dash_time -= delta_time
        
        
        