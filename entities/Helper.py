from entities.Entity import Entity


class Helper(Entity):
    def __init__(self):
        super().__init__()
        self.following = None
    
    def follow(self, entity):
        self.following = entity
    