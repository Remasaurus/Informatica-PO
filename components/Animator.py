from components.Component import Component


class Anim():
    def __init__(self, name, duration, time, current_time, prio):
        self.name = name
        self.duration = duration
        self.time = time
        self.prio = prio
        self.current_time = current_time
    
    def copy(self):
        return Anim(self.name, self.duration, self.time, self.current_time, self.prio)


class Animator(Component):
    def __init__(self, default="idle"):
        self.anims = dict()
        self.current_frame = ""
        self.default = default
        self.total_time = 0
        
    
    def add_anim(self, name, duration, time, prio):
        self.anims["name"] = Anim(name, duration, time, self.total_time, prio)
    
    
    def get_frame(self):
        if self.current_frame.time == 0:
            frame = self.current_frame.copy()
            frame.time = self.total_time - frame.current_time
            return frame
        else:
            return self.current_frame
    
    
    def update(self, entity, delta_time, level):
        self.total_time += delta_time
        best_frame = Anim(self.default, 0, 0, self.total_time, -1)
        
        for anim in self.anims.values():
            anim.duration -= delta_time
            if anim.duration < 0:
                self.anims.pop(anim.name)
            else:
                if anim.prio > best_frame.prio:
                    best_frame = anim
        

        self.current_frame = best_frame