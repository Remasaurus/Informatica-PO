from components.Component import Component


class Move(Component):
    def __init__(self):
        self.dir = 0
        self.distance = 0

        self.drag = 2.5
        self.acc = 1000
        self.dec = 600

        self.run = False

    def update(self, entity, delta_time, level):
        absX = abs(entity.vel.x)
        
        if entity.vel.x < 0:
            entity.flip = True
        elif entity.vel.x > 0:
            entity.flip = False
            
        if absX < 0.01:
            if "run" in entity.components["Animator"].anims:
                entity.components["Animator"].delete_anim("run") 
        else:
            entity.components["Animator"].add_anim("run", 1, self.distance, 0)
            
            
        
        
        if self.dir:
            acc = self.dir * self.acc * delta_time
            entity.vel.x += acc
            if self.run:
                entity.vel.x += acc/5

        elif not entity.vel.x == 0:
            decel = min(absX, self.dec * delta_time)
            if entity.vel.x < 0:
                entity.vel.x += decel
                if self.dir > 0:
                    pass
                    # entity.components["Animator"].add_anim("break", 1, self.distance, 0)
                    
            else:
                entity.vel.x -= decel
                if self.dir > 0:
                    pass
                    # entity.components["Animator"].add_anim("break", 1, self.distance, 0)
                    
                
        else:
            self.distance = 0

        drag = self.drag * delta_time * entity.vel.x

        if self.run:
            entity.vel.x -= drag/1.5
        else:
            entity.vel.x -= drag

        self.distance += absX * delta_time
