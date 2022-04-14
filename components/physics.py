from components.Component import Component


class Physics(Component):
    def __init__(self):
        self.gravity_multiplier = 1
        
    def update(self, entity, delta_time, level):
        entity.pos.x += entity.vel.x * delta_time
        level.collider.checkX(entity, level)

        entity.pos.y += entity.vel.y * delta_time
        level.collider.checkY(entity, level)

        entity.vel.y += level.gravity * delta_time * self.gravity_multiplier
        self.gravity_multiplier = 1
