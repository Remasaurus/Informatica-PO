from math import ceil, floor


class Helper():
    def __init__(self, x1, x2, y1, y2, val):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.val = val


class Grid():
    def __init__(self, tile_size):
        self.grid = []
        self.tile_size = tile_size

    def to_index(self, pos) -> int:
        return floor(pos/self.tile_size)

    def to_index_range(self, pos1, pos2):
        end = ceil(pos2/self.tile_size) * self.tile_size
        ran = []
        start = int(pos1)

        for pos in range(start, end, self.tile_size):
            ran.append(self.to_index(pos))

        return ran

    def get_by_index(self, x, y):
        tile = self.get(x, y)

        return Helper(x * self.tile_size, (x+1) * self.tile_size, y * self.tile_size, (y+1) * self.tile_size, tile)

    def get_by_range(self, x1, x2, y1, y2):
        matches = []

        for i in self.to_index_range(x1, x2):
            for j in self.to_index_range(y1, y2):
                matches.append(self.get_by_index(i, j))

        return matches

    def set(self, x, y, val):
        if len(self.grid) <= x:
            self.grid += [[] for _ in range(x - len(self.grid) + 1)]

        if len(self.grid[x]) <= y:
            self.grid[x] += [None] * (y - len(self.grid[x]) + 1)

        self.grid[x][y] = val

    def get_col(self, x):
        if len(self.grid) <= x:
            return []

        return self.grid[x]

    def get(self, x, y):
        if len(self.grid) <= x:
            return None

        if len(self.grid[x]) <= y:
            return None

        return self.grid[x][y]
