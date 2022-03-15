from components.Component import Component, Sides


class Jump(Component):
    def __init__(self):
        # Height of the jump
        self.force = 300

        # How long the player can press the jump key for more height
        self.duration = 0.2

        # How much the x velocity affects the jump
        self.boost = 0.02

        # How long the jump buffers in the air
        self.grace_period = 0.1

        # How long the player can jump while running off the edge
        self.coyote_duration = 0.1

        # helper variables
        self.request_time = 0
        self.engage_time = 0
        self.coyote_time = 0

    def start(self):
        self.request_time = self.grace_period

    def cancel(self):
        self.request_time = 0
        self.engage_time = 0

    def obstruct(self, entity, side):
        if side == Sides.BOTTOM:
            self.coyote_time = self.coyote_duration
        elif side == Sides.TOP:
            self.cancel()

    def update(self, entity, delta_time, level):
        if self.request_time > 0:
            if self.coyote_time > 0:
                self.engage_time = self.duration
                self.request_time = 0
                self.coyote_time = 0

            self.request_time -= delta_time

        if self.engage_time > 0:
            entity.vel.y = -(self.force + (abs(entity.vel.x) * self.boost))
            self.engage_time -= delta_time

        self.coyote_time -= delta_time
