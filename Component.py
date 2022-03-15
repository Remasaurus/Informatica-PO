from enum import Enum, auto


class Sides(Enum):
    LEFT = auto()
    RIGHT = auto()
    TOP = auto()
    BOTTOM = auto()


class Component():
    def __init__(self):
        pass

    def obstruct(self, entity, side):
        pass

    def update(self, entity, delta_time, level):
        pass
