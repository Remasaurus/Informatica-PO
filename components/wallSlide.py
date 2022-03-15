from components.Component import Component, Sides

class WallSlide(Component):
    def __init__(self):
        pass

    def obstruct(self, entity, side):
        if side == Sides.LEFT or side == Sides.RIGHT:
            if entity.vel.y < 0:
                pass
                #entity.vel.y *= 0.8