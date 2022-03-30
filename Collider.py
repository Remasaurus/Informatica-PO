from components.Component import Sides
from Grid import Grid

class Collider():
    """Contains all tiles in the level and handles interactions."""
    def __init__(self, tile_size) -> None:
        self.grid = Grid(tile_size)

    def checkX(self, entity, level):
        """Checks if entity had collided when any tiles on the x-axis."""    
        if entity.vel.x > 0:
            x = entity.pos.x + entity.size.x
        elif entity.vel.x < 0:
            x = entity.pos.x
        else:
            return
        for match in self.grid.get_by_range(x, x, entity.pos.y, entity.pos.y + entity.size.y):
            if match.val == "solid":
                if entity.vel.x > 0:
                    if entity.pos.x + entity.size.x > match.x1:
                        entity.pos.x = match.x1 - entity.size.x
                        entity.vel.x = 0
                        entity.obstruct(Sides.RIGHT)

                elif entity.vel.x < 0:
                    if entity.pos.x < match.x2:
                        entity.pos.x = match.x2
                        entity.vel.x = 0
                        entity.obstruct(Sides.LEFT)
            
            elif match.val == "coin":
                if "CoinCollector" in entity.components:
                    x, y = self.grid.to_index(match.x1), self.grid.to_index(match.y1)
                    self.grid.set(x, y, None)
                    level.compositor.layers["BackgroundLayer"].grid.set(x, y, None)
                    level.compositor.layers["BackgroundLayer"].redraw = True
                    entity.components["CoinCollector"].coins += 1
                    

    def checkY(self, entity, level):
        """Checks if entity had collided when any tiles on the y-axis."""
        if entity.vel.y > 0:
            y = entity.pos.y + entity.size.y
        elif entity.vel.y < 0:
            y = entity.pos.y
        else:
            return

        for match in self.grid.get_by_range(entity.pos.x, entity.pos.x + entity.size.x, y, y):
            if match.val == "solid":
                if entity.vel.y > 0:
                    if entity.pos.y + entity.size.y > match.y1:
                        entity.pos.y = match.y1 - entity.size.y
                        entity.vel.y = 0
                        entity.obstruct(Sides.BOTTOM)

                elif entity.vel.y < 0:
                    if entity.pos.y < match.y2:
                        entity.pos.y = match.y2
                        entity.vel.y = 0
                        entity.obstruct(Sides.TOP)
            elif match.val == "coin":
                if "CoinCollector" in entity.components:
                    x, y = self.grid.to_index(match.x1), self.grid.to_index(match.y1)
                    self.grid.set(x, y, None)
                    level.compositor.layers["BackgroundLayer"].grid.set(x, y, None)
                    level.compositor.layers["BackgroundLayer"].redraw = True
                    
                    entity.components["CoinCollector"].coins += 1
                    