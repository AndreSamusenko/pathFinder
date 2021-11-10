from grid import Grid
from graph import Graph
import pygame


def game_scene(func):
    def wrapper(self, *arg, **kw):
        stop_game = False
        while not stop_game:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            stop_game = func(self, *arg, **kw)

            self.clock.tick(PathFinder.FPS)
            pygame.display.update()

        # return res

    return wrapper


class PathFinder:
    WIDTH, HEIGHT = 600, 600  # размеры игрового окна
    FPS = 15

    def __init__(self):
        self.grid = Grid(10, 10)
        self.grid.randomize()
        self.graph = Graph(self.grid)

        self.cell_width = self.WIDTH // self.grid.width
        self.cell_height = self.HEIGHT // self.grid.height
        self.cell_border = 2

        self.pygame_init()
        self.path = self.graph.bfs((0, 0), (8, 8))
        self.select_game()
        # print(*sorted(graph.adjacent_vertices.items()), sep="\n")
        # path = graph.bfs((0, 0), (4, 3))

    def pygame_init(self):
        pygame.init()
        pygame.display.set_caption("Name")
        self.screen = pygame.display.set_mode((PathFinder.WIDTH, PathFinder.HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 36)

    def draw_edges(self):
        for vertex in self.graph.adjacent_vertices:
            for point in self.graph.adjacent_vertices[vertex]:
                v_x, v_y = vertex
                p_x, p_y = point
                pygame.draw.line(self.screen, pygame.Color('red'), (v_x * 60 + 28, v_y * 60 + 28),
                                 (p_x * 60 + 28, p_y * 60 + 28), width=5)

    def draw_cell(self, color, x, y):
        pygame.draw.rect(self.screen, color, pygame.Rect(x * self.cell_width + self.cell_border,
                                                         y * self.cell_height + self.cell_border,
                                                         self.cell_width - 2 * self.cell_border,
                                                         self.cell_height - 2 * self.cell_border))

    def draw_grid(self):
        for i in range(self.grid.width):
            for j in range(self.grid.height):
                if (i, j) in self.path:
                    color = pygame.Color('white')
                elif not self.grid.cells[i][j]:
                    color = pygame.Color('green')
                else:
                    color = pygame.Color('orange')
                self.draw_cell(color, i, j)

    def _count_mouse_pos(self):
        cell_width = self.WIDTH // self.grid.width
        cell_height = self.HEIGHT // self.grid.height

        m_x, m_y = pygame.mouse.get_pos()
        m_x //= cell_width
        m_y //= cell_height

        return m_x, m_y

    @game_scene
    def select_game(self):
        self.draw_grid()
        # self.draw_edges()

        m_x, m_y = self._count_mouse_pos()
        if self.grid.cells[m_x][m_y] == Grid.EMPTY_CELL:
            self.draw_cell(pygame.color.Color("pink"), m_x, m_y)

            clicked = pygame.mouse.get_pressed()[0]
            if clicked:
                self.path = self.graph.bfs((0, 0), (m_x, m_y))


game = PathFinder()
