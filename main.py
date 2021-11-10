from grid import Grid
from graph import Graph
import pygame


def game_scene(func):
    def wrapper(self, *arg, **kw):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            res = func(self, *arg, **kw)

            self.clock.tick(PathFinder.FPS)
            pygame.display.update()

            if res:
                break
        # return res
    return wrapper


class PathFinder:
    WIDTH, HEIGHT = 600, 600  # размеры игрового окна
    FPS = 5

    def __init__(self):
        self.grid = Grid(10, 10)
        self.grid.randomize()
        self.graph = Graph(self.grid)
        self.pygame_init()
        self.path = self.graph.bfs((0, 0), (8, 8))
        self.select_game()
        # print(*sorted(graph.adjacent_vertices.items()), sep="\n")
        # path = graph.bfs((0, 0), (4, 3))

    def pygame_init(self):
        pygame.init()  # объявляем использование библиотеки pygame
        pygame.display.set_caption("Name")  # название окна
        self.screen = pygame.display.set_mode((PathFinder.WIDTH, PathFinder.HEIGHT))  # создаём игровое окно
        self.clock = pygame.time.Clock()  # создаём таймер
        self.font = pygame.font.SysFont('arial', 36)  # шрифт

    def draw_edges(self):
        for vertex in self.graph.adjacent_vertices:
            for point in self.graph.adjacent_vertices[vertex]:
                v_x, v_y = vertex
                p_x, p_y = point
                pygame.draw.line(self.screen, pygame.Color('red'), (v_x * 60 + 28, v_y * 60 + 28),
                                 (p_x * 60 + 28, p_y * 60 + 28), width=5)

    # def draw_game(self):
    #     path = self.graph.bfs((0, 0), (8, 8))
    #
    #     while True:
    #         events = pygame.event.get()
    #         for event in events:
    #             if event.type == pygame.QUIT:
    #                 exit()
    #         for i in range(10):
    #             for j in range(10):
    #                 if (i, j) in path:
    #                     color = pygame.Color('white')
    #                 elif not self.grid.cells[i][j]:
    #                     color = pygame.Color('green')
    #                 else:
    #                     color = pygame.Color('orange')
    #                 pygame.draw.rect(self.screen, color, pygame.Rect(i * 60 + 2, j * 60 + 2, 56, 56))
    #         # self.draw_edges()
    #         self.clock.tick(PathFinder.FPS)
    #         pygame.display.update()

    def draw_grid(self):
        cell_width = self.WIDTH // self.grid.width
        cell_height = self.HEIGHT // self.grid.height
        cell_border = 2

        for i in range(10):
            for j in range(10):
                if (i, j) in self.path:
                    color = pygame.Color('white')
                elif not self.grid.cells[i][j]:
                    color = pygame.Color('green')
                else:
                    color = pygame.Color('orange')
                pygame.draw.rect(self.screen, color, pygame.Rect(i * cell_width + cell_border,
                                                                 j * cell_height + cell_border,
                                                                 cell_width - 2 * cell_border,
                                                                 cell_height - 2 * cell_border))

    @game_scene
    def select_game(self):
        self.draw_grid()


        # self.draw_edges()
        # return True


game = PathFinder()
