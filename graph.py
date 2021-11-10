from grid import Grid
from collections import deque


class Graph:
    def __init__(self, grid: Grid):
        self.adjacent_vertices = {}
        self._make_graph(grid)

    def _make_graph(self, grid):
        for x in range(grid.width):
            for y in range(grid.height):
                if grid.cells[x][y] == grid.EMPTY_CELL:
                    self.adjacent_vertices[(x, y)] = grid.get_neighbours(x, y)

    def __str__(self):
        return str(self.adjacent_vertices)

    def bfs(self, start, finish):
        queue = deque([start])
        visited = {start: None}

        while queue:
            cur_node = queue.popleft()
            if cur_node == finish:
                break

            next_nodes = self.adjacent_vertices[cur_node]
            for next_node in next_nodes:
                if next_node not in visited:
                    queue.append(next_node)
                    visited[next_node] = cur_node

        path = [finish]

        vertex = finish
        while vertex and vertex in visited:
            vertex = visited[vertex]
            if vertex:
                path.append(vertex)
        return path[::-1]
