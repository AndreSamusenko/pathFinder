import random


class Grid:
    RANDOM_COEFFICIENT = 2
    EMPTY_CELL = 0
    FILLED_CELL = 1

    def __init__(self, width, height, diag_dir=False):
        self.width = width
        self.height = height
        self.diag_dir = diag_dir
        self.cells = [[Grid.EMPTY_CELL] * self.width for _ in range(self.height)]

    def set_value(self, x, y, value):
        if not self.check_indexes(x, y):
            raise IndexError("Invalid index")

        self.cells[x][y] = value

    def randomize(self):
        random_floor = 0
        random_ceil = 10

        for i in range(self.height):
            for j in range(self.width):
                self.cells[i][j] = Grid.EMPTY_CELL \
                    if random.randint(random_floor, random_ceil) > Grid.RANDOM_COEFFICIENT \
                    else Grid.FILLED_CELL
        self.cells[0][0] = 0

    def check_indexes(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def check_neighbors(self, x, y):
        return self.check_indexes(x, y) and not self.cells[x][y]

    def get_neighbours(self, x, y):
        directions = {(-1, 0), (0, -1), (1, 0), (0, 1)}
        if self.diag_dir:
            directions.update((-1, -1), (1, -1), (1, 1), (-1, 1))

        neighbors = []
        for x_dir, y_dir in directions:
            neighbor = x + x_dir, y + y_dir
            if self.check_neighbors(*neighbor):
                neighbors.append(neighbor)

        return neighbors

    def __str__(self):
        return str(self.cells)
