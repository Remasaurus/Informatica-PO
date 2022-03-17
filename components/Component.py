from enum import Enum, auto


class Sides(Enum):
    """All sides the entity can possible collide with."""
    LEFT = auto()
    RIGHT = auto()
    TOP = auto()
    BOTTOM = auto()


class Component():
    """Baseclass for all components."""
    def __init__(self):
        pass

    def obstruct(self, entity, side):
        pass

    def update(self, entity, delta_time, level):
        pass
