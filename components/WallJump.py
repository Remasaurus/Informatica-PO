


from components.Component import Component


class WallJump(Component):
    def __init__(self):
      
      self.force = 300
      self.duration = 0.2
      self.grace_period = 0.1
      self.coyote_duration = 0.1

      self.request_time = 0
      self.engage_time = 0
      self.coyote_time = 0

    def start(self):
      self.request_time = self.grace_period

    def cancel(self):
      self.request_time = 0
      self.engage_time = 0

    def obstruct(self, entity, side):
      if side == side.LEFT or side == side.RIGHT:
        self.coyote_time = self.coyote_duration

      elif side == side.TOP:
        self.cancel


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
        
