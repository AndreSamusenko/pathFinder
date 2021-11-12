import pygame
from grid import Grid
from graph import Graph


def game_scene(func):
    def wrapper(self, *arg, **kw):
        stop_game = False
        while not stop_game:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
            self.screen.fill((0, 0, 0))
            stop_game = func(self, events, *arg, **kw)

            self.clock.tick(PathFinder.FPS)
            pygame.display.update()
    return wrapper


class PathFinder:
    WIDTH, HEIGHT = 800, 800  # размеры игрового окна
    FPS = 15
    CELLS_NUM = 10
    MAX_CELLS_SIZE = 100
    MIN_CELLS_SIZE = 10

    EMPTY_COLOR = pygame.Color("#00BF32")
    OBSTACLE_COLOR = pygame.Color("#FF9900")
    START_COLOR = pygame.Color("#1D766F")
    FINISH_COLOR = pygame.Color("#00665E")
    NO_WAY_COLOR = pygame.Color("#FF2C00")
    WAY_COLOR = pygame.Color("#5DCEC6")
    EDGES_COLOR = pygame.Color("#399200")
    SELECT_COLOR = pygame.Color("#FFFF73")
    DELETE_COLOR = pygame.Color("#696969")

    START_MODE = "START"
    FINISH_MODE = "FINISH"
    ADD_MODE = "ADD"
    DELETE_MODE = "DELETE"

    def __init__(self):
        self.grid = Grid(PathFinder.CELLS_NUM, PathFinder.CELLS_NUM)
        self.grid.randomize()
        self.graph = Graph(self.grid)
        self.start = (0, 0)
        self.finish = (5, 5)
        self.has_diag_dirs = False
        self.select_mode = PathFinder.FINISH_MODE

        self.__recount_cell_size()
        self.show_edges = False

        self.screen = None
        self.clock = None
        self.font = None
        self.pygame_init()
        self.path = {}
        self.select_game()

    def pygame_init(self):
        pygame.init()
        pygame.display.set_caption("Path Finder")
        self.screen = pygame.display.set_mode((PathFinder.WIDTH, PathFinder.HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 36)

    def draw_edges(self):
        for vertex in self.graph.adjacent_vertices:
            for point in self.graph.adjacent_vertices[vertex]:
                v_x, v_y = vertex
                p_x, p_y = point
                pygame.draw.line(self.screen, PathFinder.NO_WAY_COLOR, (v_x * self.cell_width + self.cell_width // 2,
                                                                        v_y * self.cell_height + self.cell_height // 2),
                                 (p_x * self.cell_width + self.cell_width // 2,
                                  p_y * self.cell_height + self.cell_height // 2),
                                 width=1)

    def draw_cell(self, color, x, y):
        pygame.draw.rect(self.screen, color, pygame.Rect(x * self.cell_width + self.cell_border,
                                                         y * self.cell_height + self.cell_border,
                                                         self.cell_width - 2 * self.cell_border,
                                                         self.cell_height - 2 * self.cell_border))

    def draw_grid(self):
        for i in range(self.grid.width):
            for j in range(self.grid.height):
                if (i, j) in self.path:
                    if (i, j) == self.start:
                        color = PathFinder.START_COLOR
                    elif len(self.path) == 1:
                        color = PathFinder.NO_WAY_COLOR
                    elif (i, j) == self.finish:
                        color = PathFinder.FINISH_COLOR
                    else:
                        color = PathFinder.WAY_COLOR
                elif not self.grid.cells[i][j]:
                    color = PathFinder.EMPTY_COLOR
                else:
                    color = PathFinder.OBSTACLE_COLOR
                self.draw_cell(color, i, j)

    def _count_mouse_pos(self):
        cell_width = self.WIDTH // self.grid.width
        cell_height = self.HEIGHT // self.grid.height

        m_x, m_y = pygame.mouse.get_pos()
        m_x //= cell_width
        m_y //= cell_height

        return m_x, m_y

    def __recount_cell_size(self):
        self.cell_width = self.WIDTH // self.grid.width
        self.cell_height = self.HEIGHT // self.grid.height
        self.cell_border = int(self.cell_width * 0.05)

    def replace_start(self, m_x, m_y):
        self.start = (m_x, m_y)
        self.path = self.graph.bfs(self.start, self.finish)

    def replace_finish(self, m_x, m_y):
        self.finish = (m_x, m_y)
        self.path = self.graph.bfs(self.start, self.finish)

    def __change_cells(self, m_x, m_y, value):
        if self.grid.check_indexes(m_x, m_y) and self.grid.cells[m_x][m_y] != value:
            self.grid.set_value(m_x, m_y, value)
            self.graph = Graph(self.grid)
            self.path.clear()

    def add_new_obstacles(self, m_x, m_y):
        self.__change_cells(m_x, m_y, Grid.FILLED_CELL)

    def delete_obstacles(self, m_x, m_y):
        self.__change_cells(m_x, m_y, Grid.EMPTY_CELL)

    def change_show_edges(self):
        self.show_edges = not self.show_edges

    def randomize_map(self):
        self.grid.randomize()
        self.graph = Graph(self.grid)
        self.path.clear()

    def __recreate_grid(self):
        self.grid = Grid(self.CELLS_NUM, self.CELLS_NUM, self.has_diag_dirs)
        self.grid.randomize()
        self.graph = Graph(self.grid)
        self.__recount_cell_size()
        self.path.clear()

    def increase_cells_count(self):
        if self.CELLS_NUM < PathFinder.MAX_CELLS_SIZE:
            self.CELLS_NUM *= 2
            self.__recreate_grid()

    def decrease_cells_count(self):
        if self.CELLS_NUM > PathFinder.MIN_CELLS_SIZE:
            self.CELLS_NUM //= 2
            self.__recreate_grid()

    def change_diag_dirs(self):
        self.has_diag_dirs = not self.has_diag_dirs
        self.grid.diag_dir = self.has_diag_dirs
        self.graph = Graph(self.grid)

    def __switch_modes(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                modes = {pygame.K_1: PathFinder.START_MODE,
                         pygame.K_2: PathFinder.FINISH_MODE,
                         pygame.K_3: PathFinder.ADD_MODE,
                         pygame.K_4: PathFinder.DELETE_MODE}

                settings = {pygame.K_5: self.change_show_edges,
                            pygame.K_6: self.randomize_map,
                            pygame.K_7: self.increase_cells_count,
                            pygame.K_8: self.decrease_cells_count,
                            pygame.K_9: self.change_diag_dirs}

                if event.key in modes.keys():
                    self.select_mode = modes[event.key]
                    print(self.select_mode)
                elif event.key in settings:
                    settings[event.key]()
                    print(settings[event.key])

    def __make_action_on_click(self):
        m_x, m_y = self._count_mouse_pos()
        if self.grid.cells[m_x][m_y] == Grid.EMPTY_CELL or self.select_mode == PathFinder.DELETE_MODE:
            self.draw_cell(PathFinder.SELECT_COLOR, m_x, m_y)

            if clicked := pygame.mouse.get_pressed()[0]:
                actions = {PathFinder.FINISH_MODE: self.replace_finish,
                           PathFinder.START_MODE: self.replace_start,
                           PathFinder.ADD_MODE: self.add_new_obstacles,
                           PathFinder.DELETE_MODE: self.delete_obstacles}

                if self.select_mode in actions.keys():
                    action = actions[self.select_mode]
                    action(m_x, m_y)

    @game_scene
    def select_game(self, events):
        self.draw_grid()
        if self.show_edges:
            self.draw_edges()

        self.__switch_modes(events)
        self.__make_action_on_click()
