from components.Component import Component, Sides

class WallSlide(Component):
    def obstruct(self, entity, side):
        if side == Sides.LEFT or side == Sides.RIGHT:
            if entity.vel.y > 0:
                entity.vel.y *= 0.9