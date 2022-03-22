from entities.Entity import Entity


class Player(Entity):
    """Player class that overwrites the draw function."""
    
    def draw(self, surface, camera, spritesheet):
        spritesheet.draw("player", surface, self.pos.x -
                         camera.pos.x, self.pos.y - camera.pos.y)
