from Entity import Entity


class Player(Entity):
    def __init__(self):
        super().__init__()

    def draw(self, surface, camera, spritesheet):
        spritesheet.draw("player", surface, self.pos.x -
                         camera.pos.x, self.pos.y - camera.pos.y)
