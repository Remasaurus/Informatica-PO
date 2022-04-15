import pygame
from components.Component import Sides
from Grid import Grid
from entities.Player import Player


class DespawningTile():
    def __init__(self, x, y, time):
        self.x = x
        self.y = y
        self.time = time
        self.explored = set()


class Collider():
    """Contains all tiles in the level and handles interactions."""

    def __init__(self, tile_size) -> None:
        self.grid = Grid(tile_size)
        self.total_time = 0
        self.despawning_tiles = []
        self.explored = set()
        
    def update(self, delta_time, level):
        self.total_time += delta_time
        
        for i, tile in reversed(list(enumerate(self.despawning_tiles))):
            if self.total_time - tile.time > 2:
                self.despawning_tiles.pop(i)
                self.grid.set(tile.x, tile.y, "air")
                self.explored.remove((tile.x, tile.y))
                
                level.compositor.layers["BackgroundLayer"].grid.set(tile.x, tile.y, None)
                level.compositor.layers["BackgroundLayer"].redraw = True
                
    def despawn_tile(self, x, y):
        stack = [(x, y)]
        
        while stack:
            current_tile = stack[-1]
            has_to_explore = False
            
            for neighbour in self.get_neighbours(current_tile[0], current_tile[1]):
                if neighbour not in self.explored:
                    if self.grid.get(neighbour[0], neighbour[1]) == "despawn":
                        self.despawning_tiles.append(
                            DespawningTile(neighbour[0], neighbour[1], self.total_time)
                        )
                        self.explored.add(neighbour)
                        stack.append(neighbour)
                        has_to_explore = True
            
            if not has_to_explore:
                stack.pop(-1)
                    
        
    def get_neighbours(self, x, y):
        return [
            (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)
        ]
        
    
    def win(self, level):
        level.finished = True
        
        
            
            
        
    def handle_spike(self, spike_rect, entity):
        if pygame.Rect(entity.pos, entity.size).colliderect(spike_rect):
            entity.hit()

    def checkX(self, entity, level):
        """Checks if entity had collided when any tiles on the x-axis."""
        if entity.vel.x > 0:
            x = entity.pos.x + entity.size.x
        elif entity.vel.x < 0:
            x = entity.pos.x
        else:
            return

        for match in self.grid.get_by_range(x, x, entity.pos.y, entity.pos.y + entity.size.y):
            if match.val == "solid" or match.val == "despawn":                
                if entity.vel.x > 0:
                    left_tile = self.grid.get(self.grid.to_index(match.x1) - 1, self.grid.to_index(match.y1))
                    if entity.pos.x + entity.size.x > match.x1 and not left_tile == "solid" and not left_tile == "ramp-right":
                        entity.pos.x = match.x1 - entity.size.x
                        entity.vel.x = 0
                        entity.obstruct(Sides.RIGHT)

                elif entity.vel.x < 0:
                    right_tile = self.grid.get(self.grid.to_index(match.x1) + 1, self.grid.to_index(match.y1)) 
                    if entity.pos.x < match.x2 and not right_tile == "solid" and not right_tile == "ramp-left":
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
            
            elif match.val == "sand":
                entity.vel.x *= 0.9

            elif match.val == "ramp-right":
                if entity.vel.x > 0:
                    if self.grid.get(self.grid.to_index(entity.pos.x + entity.size.x), self.grid.to_index(entity.pos.y)) == "solid":
                        continue
                    rampY = match.y2 - \
                        ((entity.pos.x + entity.size.x) - match.x1)
                    if entity.pos.y + entity.size.y >= rampY:
                        newY = max(rampY, match.y1) - entity.size.y
                        
                        y = self.grid.to_index(newY)
                        # Check for collision in new position
                        for x in self.grid.to_index_range(entity.pos.x, entity.pos.x + entity.size.x):
                            tile = self.grid.get_by_index(x, y)
                            if tile.val == "solid":
                                entity.pos.y = tile.y2
                                entity.pos.x = match.x2 - ((tile.y2 + entity.size.y) - match.y1) - entity.size.x
                                entity.vel.x = 0
                                break
                                
                        else:
                            entity.pos.y = newY
                            entity.vel.x *= 0.96
                            
            elif match.val == "ramp-topright":
                if entity.vel.x > 0:
                    rampY = match.y1 + \
                        ((entity.pos.x + entity.size.x) - match.x1)
                    
                    if entity.pos.y < rampY:
                        entity.pos.y = rampY
                        entity.vel.x = 0
                        
                        
                        
                            
            elif match.val == "ramp-left":
                if entity.vel.x < 0:
                    if self.grid.get(self.grid.to_index(entity.pos.x), self.grid.to_index(entity.pos.y)) == "solid":
                        continue
                    rampY = match.y2 - \
                        (match.x2 - (entity.pos.x))
                    if entity.pos.y + entity.size.y >= rampY:
                        newY = max(rampY, match.y1) - entity.size.y
                        
                        y = self.grid.to_index(newY)
                        # Check for collision in new position
                        for x in self.grid.to_index_range(entity.pos.x, entity.pos.x + entity.size.x):
                            tile = self.grid.get_by_index(x, y)
                            if tile.val == "solid":
                                entity.pos.y = tile.y2
                                entity.pos.x = match.x2 - ((tile.y2 + entity.size.y) - match.y1) - entity.size.x
                                entity.vel.x = 0
                                break
                                
                        else:
                            entity.pos.y = newY
                            entity.vel.x *= 0.96
                            
            elif match.val == "ramp-topleft":
                if entity.vel.x > 0:
                    rampY = match.y1 + \
                        (match.x2 - (entity.pos.x))
                    
                    if entity.pos.y < rampY:
                        entity.pos.y = rampY
                        entity.vel.x = 0

            elif match.val == "spike-left":
                if entity.spikeable:
                    self.handle_spike(pygame.Rect(match.x1, match.y1, match.x2 - self.grid.tile_size/2, match.y2), entity)

            elif match.val == "spike-right":
                if entity.spikeable:
                    self.handle_spike(pygame.Rect(match.x1 + self.grid.tile_size/2, match.y1, match.x2, match.y2), entity)

            elif match.val == "spike-top":
                if entity.spikeable:
                    self.handle_spike(pygame.Rect(match.x1, match.y1, match.x2, match.y2 - self.grid.tile_size/2), entity)

            elif match.val == "spike-bottom":
                if entity.spikeable:
                    self.handle_spike(pygame.Rect(match.x1, match.y1 + self.grid.tile_size/2, match.x2, match.y2), entity)

            elif match.val == "finish":
                if type(entity) == Player:
                    self.win(level)


    def checkY(self, entity, level):
        """Checks if entity had collided when any tiles on the y-axis."""
        if entity.vel.y > 0:
            y = entity.pos.y + entity.size.y
        elif entity.vel.y < 0:
            y = entity.pos.y
            bottom_tiles = self.grid.get_by_range(entity.pos.x, entity.pos.x + entity.size.x,
                                                  entity.pos.y + entity.size.y, entity.pos.y + entity.size.y)
            for tile in bottom_tiles:
                if tile.val == "sand":
                    entity.vel.y *= 0.95
        else:
            return
        
        


        for match in self.grid.get_by_range(entity.pos.x, entity.pos.x + entity.size.x, y, y):
            if match.val == "solid":
                if entity.vel.y > 0:
                    if entity.pos.y + entity.size.y > match.y1:
                        entity.pos.y = match.y1 - entity.size.y
                        entity.obstruct(Sides.BOTTOM)
                        entity.vel.y = 0

                elif entity.vel.y < 0:
                    if entity.pos.y < match.y2:
                        entity.pos.y = match.y2
                        entity.vel.y = 0
                        entity.obstruct(Sides.TOP)
                        
            if match.val == "despawn":
                if entity.vel.y > 0:
                    if entity.pos.y + entity.size.y > match.y1:
                        entity.pos.y = match.y1 - entity.size.y
                        entity.vel.y = 0
                        entity.obstruct(Sides.BOTTOM)
                        x, y = self.grid.to_index(match.x1), self.grid.to_index(match.y1)
                        
                        if (x, y) not in self.explored:
                            self.despawn_tile(x, y)
                        

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

            elif match.val == "sand":
                if entity.vel.y > 0:
                    entity.vel.y *= 0.9
                
                entity.obstruct(Sides.BOTTOM)
            
            elif match.val == "ramp-right":
                if entity.vel.y > 0:
                    rampY = match.y2 - \
                        ((entity.pos.x + entity.size.x) - match.x1)
                    if entity.pos.y + entity.size.y >= rampY:
                        # So player cant dash through the thin part of the ramp
                        if self.grid.get_by_index(self.grid.to_index(match.x1) + 1, self.grid.to_index(
                                match.y1) - 1).val == "ramp":
                            entity.pos.y = rampY - entity.size.y
                        else:
                            entity.pos.y = max(rampY, match.y1) - entity.size.y

                        entity.vel.y = 0
                        entity.obstruct(Sides.BOTTOM)
            
            elif match.val == "ramp-topright":
                if entity.vel.y < 0:
                    rampY = match.y2 - \
                        (match.x2 - (entity.pos.x + entity.size.x))

                    if entity.pos.y < rampY:
                        newX = max(match.x1 + (entity.pos.y - match.y1), match.x1) - entity.size.x
                        entity.pos.x = newX
                        entity.vel.y *= 0.96
                        
            elif match.val == "ramp-left":
                if entity.vel.y > 0:
                    rampY = match.y2 - \
                        (match.x2 - (entity.pos.x))
                    if entity.pos.y + entity.size.y >= rampY:
                        # So player cant dash through the thin part of the ramp
                        if self.grid.get_by_index(self.grid.to_index(match.x1) + 1, self.grid.to_index(
                                match.y1) - 1).val == "ramp":
                            entity.pos.y = rampY - entity.size.y
                        else:
                            entity.pos.y = max(rampY, match.y1) - entity.size.y

                        entity.vel.y = 0
                        entity.obstruct(Sides.BOTTOM)
            
            elif match.val == "ramp-topleft":
                if entity.vel.y < 0:
                    rampY = match.y1 + \
                        (match.x2 - (entity.pos.x))
                    
                    if entity.pos.y < rampY:
                        newX = min(match.x2 - (entity.pos.y - match.y1), match.x2)
                        
                        x = self.grid.to_index(newX)
                        # Check for collision in new position
                        for y in self.grid.to_index_range(entity.pos.x, entity.pos.x + entity.size.x):
                            tile = self.grid.get_by_index(x, y)
                            if tile.val == "solid":
                                entity.pos.x = tile.x1 - entity.size.x
                                entity.pos.y = match.x2 - ((tile.y2 + entity.size.y) - match.y1) - entity.size.x
                                entity.vel.y = 0
                                break
                        else:
                            entity.pos.x = newX
                            entity.vel.y *= 0.96
                            
                        
            

            elif match.val == "spike-left":
                if entity.spikeable:
                    self.handle_spike(pygame.Rect(match.x1, match.y1, match.x2 - self.grid.tile_size/2, match.y2), entity)

            elif match.val == "spike-right":
                if entity.spikeable:
                    self.handle_spike(pygame.Rect(match.x1 + self.grid.tile_size/2, match.y1, match.x2, match.y2), entity)

            elif match.val == "spike-top":
                if entity.spikeable:
                    self.handle_spike(pygame.Rect(match.x1, match.y1, match.x2, match.y2 - self.grid.tile_size/2), entity)

            elif match.val == "spike-bottom":
                if entity.spikeable:
                    self.handle_spike(pygame.Rect(match.x1, match.y1 + self.grid.tile_size/2, match.x2, match.y2), entity)
                    
            elif match.val == "finish":
                if type(entity) == Player:
                    self.win(level)