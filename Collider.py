from components.Component import Sides
from Grid import Grid


class Collider():

    def __init__(self, tile_size) -> None:
        self.grid = Grid(tile_size)

    def checkX(self, entity):
        if entity.vel.x > 0:
            x = entity.pos.x + entity.size.x
        elif entity.vel.x < 0:
            x = entity.pos.x
        else:
            return

        for match in self.grid.get_by_range(x, x, entity.pos.y, entity.pos.y + entity.size.y):
            if not match.val == "solid":
                continue

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

    def checkY(self, entity):
        if entity.vel.y > 0:
            y = entity.pos.y + entity.size.y
        elif entity.vel.y < 0:
            y = entity.pos.y
        else:
            return

        for match in self.grid.get_by_range(entity.pos.x, entity.pos.x + entity.size.x, y, y):
            if not match.val == "solid":
                continue

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
