from components.Component import Sides
from Grid import Grid


def sort_func(e):
    return e.val if e.val is not None else "z"


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

        a = sorted(self.grid.get_by_range(x, x, entity.pos.y,
                                          entity.pos.y + entity.size.y), key=sort_func)

        for match in a:
            if match.val is None:
                break

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
                    indexX, indexY = self.grid.to_index(
                        match.x1), self.grid.to_index(match.y1)
                    self.grid.set(indexX, indexY, None)
                    level.compositor.layers["BackgroundLayer"].grid.set(
                        indexX, indexY, None)
                    level.compositor.layers["BackgroundLayer"].redraw = True
                    entity.components["CoinCollector"].coins += 1

            elif match.val == "ramp":
                if entity.vel.x > 0:
                    rampY = match.y2 - \
                        ((entity.pos.x + entity.size.x) - match.x1)
                    if entity.pos.y + entity.size.y >= rampY:
                        if not self.grid.get_by_index(self.grid.to_index(match.x1), self.grid.to_index(
                                match.y1) - 1).val == "solid" and not self.grid.get_by_index(self.grid.to_index(match.x1) - 1, self.grid.to_index(
                                match.y1) - 1).val == "solid":

                            entity.pos.y = max(rampY, match.y1) - entity.size.y
                            entity.vel.x *= 0.96
                        else:
                            entity.pos.x = match.x1 - entity.size.x
                            entity.vel.x = 0

                        break

                # elif entity.vel.x < 0:
                #     entity.pos.x = match.x2
                #     entity.vel.x = 0
                #     entity.obstruct(Sides.LEFT)

            elif match.val == "spike-left":
                pass

            elif match.val == "spike-right":
                pass

            elif match.val == "spike-top":
                pass

            elif match.val == "spike-bottom":
                pass

    def checkY(self, entity, level):
        """Checks if entity had collided when any tiles on the y-axis."""
        if entity.vel.y > 0:
            y = entity.pos.y + entity.size.y
        elif entity.vel.y < 0:
            y = entity.pos.y
        else:
            return

        a = sorted(self.grid.get_by_range(
            entity.pos.x, entity.pos.x + entity.size.x, y, y), key=sort_func)

        if type(entity).__name__ == "Player":
            print([b.val for b in a])
        for match in a:
            if match.val is None:
                break

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
                    indexX, indexY = self.grid.to_index(
                        match.x1), self.grid.to_index(match.y1)
                    self.grid.set(indexX, indexY, None)
                    level.compositor.layers["BackgroundLayer"].grid.set(
                        indexX, indexY, None)
                    level.compositor.layers["BackgroundLayer"].redraw = True

                    entity.components["CoinCollector"].coins += 1

            elif match.val == "ramp":
                if entity.vel.y > 0:
                    rampY = match.y2 - \
                        ((entity.pos.x + entity.size.x) - match.x1)
                    if entity.pos.y + entity.size.y >= rampY:
                        if self.grid.get_by_index(self.grid.to_index(match.x1) + 1, self.grid.to_index(
                                match.y1) - 1).val == "ramp":
                            entity.pos.y = rampY - entity.size.y
                        else:
                            entity.pos.y = max(rampY, match.y1) - entity.size.y

                        entity.vel.y = 0
                        entity.obstruct(Sides.BOTTOM)
                        break

            elif match.val == "spike-left":
                pass

            elif match.val == "spike-right":
                pass

            elif match.val == "spike-top":
                pass

            elif match.val == "spike-bottom":
                pass
