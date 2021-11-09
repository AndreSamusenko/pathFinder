from grid import Grid
from graph import Graph
import pygame


class PathFinder:
    WIDTH, HEIGHT = 600, 600  # размеры игрового окна
    FPS = 10

    def __init__(self):
        self.grid = Grid(10, 10)
        self.grid.randomize()
        self.graph = Graph(self.grid)
        self.pygame_init()
        self.draw_game()
        # print(*sorted(graph.adjacent_vertices.items()), sep="\n")
        # path = graph.bfs((0, 0), (4, 3))

    def pygame_init(self):
        pygame.init()  # объявляем использование библиотеки pygame
        pygame.display.set_caption("Name")  # название окна
        self.screen = pygame.display.set_mode((PathFinder.WIDTH, PathFinder.HEIGHT))  # создаём игровое окно
        self.clock = pygame.time.Clock()  # создаём таймер
        self.font = pygame.font.SysFont('arial', 36)  # шрифт

    def draw_game(self):
        path = self.graph.bfs((0, 0), (4, 3))

        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
            for i in range(10):
                for j in range(10):
                    if (i, j) in path:
                        pygame.draw.rect(self.screen, pygame.Color('white'), pygame.Rect(i * 60 + 2, j*60 + 2, 48, 48))
                    elif not self.grid.cells[i][j]:
                        pygame.draw.rect(self.screen, pygame.Color('green'), pygame.Rect(i * 60, j * 60 + 2, 48, 48))
                    else:
                        pygame.draw.rect(self.screen, pygame.Color('orange'), pygame.Rect(i * 60, j * 60 + 2, 48, 48))

            self.clock.tick(PathFinder.FPS)
            pygame.display.update()


game = PathFinder()
