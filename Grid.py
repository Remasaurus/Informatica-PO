from math import ceil, floor


class Helper():
    """Wrapper for easier acces."""

    def __init__(self, x1, x2, y1, y2, val):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.val = val


class Grid():
    """Matrix that holds values, and has helper functions for tile based games."""

    def __init__(self, tile_size):
        self.grid = []
        self.tile_size = tile_size

    def to_index(self, pos) -> int:
        """Returns index to find tile."""
        return floor(pos/self.tile_size)

    def to_index_range(self, pos1, pos2):
        """Returns all indices in the given range."""
        return range(floor(pos1/self.tile_size), ceil(pos2/self.tile_size))

    def get_by_index(self, x, y):
        """Gets value from grid at given location."""
        tile = self.get(x, y)

        return Helper(x * self.tile_size, (x+1) * self.tile_size, y * self.tile_size, (y+1) * self.tile_size, tile)

    def get_by_range(self, x1, x2, y1, y2):
        """returns all values in the given square."""
        matches = []

        for i in self.to_index_range(x1, x2):
            for j in self.to_index_range(y1, y2):
                matches.append(self.get_by_index(i, j))

        return matches

    def set(self, x, y, val):
        """Set value in given location."""
        if len(self.grid) <= x:
            self.grid += [[] for _ in range(x - len(self.grid) + 1)]

        if len(self.grid[x]) <= y:
            self.grid[x] += [None] * (y - len(self.grid[x]) + 1)

        self.grid[x][y] = val

    def get_col(self, x):
        """Returns col array."""
        if len(self.grid) <= x:
            return []

        return self.grid[x]

    def get(self, x, y):
        """Return value at given index."""
        if len(self.grid) <= x or x < 0:
            return None

        if len(self.grid[x]) <= y or y < 0:
            return None

        return self.grid[x][y]
