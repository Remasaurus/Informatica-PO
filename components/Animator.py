from components.Component import Component


class Anim():
    def __init__(self, name, duration, time, prio):
        self.name = name
        self.duration = duration
        self.time = time
        self.prio = prio


class Animator(Component):
    def __init__(self, default="idle"):
        self.anims = dict()
        self.current_frame = ""
        self.default = default
        
    
    def add_anim(self, name, duration, time, prio):
        self.anims["name"] = Anim(name, duration, time, prio)
    
    
    def get_frame(self):
        return self.current_frame
    
    
    def update(self, entity, delta_time, level):
        best_frame = ["", -1]
        
        for anim in self.anims.values():
            anim.duration -= delta_time
            if anim.duration < 0:
                self.anims.pop(anim.name)
            else:
                if anim.prio > best_frame[1]:
                    best_frame = [anim.name, anim.prio, anim.time]
        
        if best_frame[1] == -1:
            self.current_frame = [self.default, 0]
        else:
            self.current_frame = best_frame