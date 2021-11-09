import pygame as pg
from random import random
from collections import deque


def get_next_nodes(x, y):
    check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows and not grid[y][x] else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
    return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]


cols, rows = 35, 20

# grid
grid = [[1 if random() < 0.2 else 0 for col in range(cols)] for row in range(rows)]
# dict of adjacency lists
graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        if not col:
            graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)

# BFS settings
start = (0, 0)
goal = start
queue = deque([start])
visited = {start: None}
print(*sorted(graph.items()), sep="\n")
# while True:
#     # fill screen
#     sc.fill(pg.Color('black'))
#     # draw grid
#     [[pg.draw.rect(sc, pg.Color('darkorange'), get_rect(x, y), border_radius=TILE // 5)
#       for x, col in enumerate(row) if col] for y, row in enumerate(grid)]
#     # draw BFS work
#     [pg.draw.rect(sc, pg.Color('forestgreen'), get_rect(x, y)) for x, y in visited]
#     [pg.draw.rect(sc, pg.Color('darkslategray'), get_rect(x, y)) for x, y in queue]
#
#     # bfs, get path to mouse click
#     mouse_pos = get_click_mouse_pos()
#     if mouse_pos and not grid[mouse_pos[1]][mouse_pos[0]]:
#         queue, visited = bfs(start, mouse_pos, graph)
#         goal = mouse_pos
#
#     # draw path
#     path_head, path_segment = goal, goal
#     while path_segment and path_segment in visited:
#         pg.draw.rect(sc, pg.Color('white'), get_rect(*path_segment), TILE, border_radius=TILE // 3)
#         path_segment = visited[path_segment]
#     pg.draw.rect(sc, pg.Color('blue'), get_rect(*start), border_radius=TILE // 3)
#     pg.draw.rect(sc, pg.Color('magenta'), get_rect(*path_head), border_radius=TILE // 3)
#     # pygame necessary lines
#     [exit() for event in pg.event.get() if event.type == pg.QUIT]
#     pg.display.flip()
#     clock.tick(30)