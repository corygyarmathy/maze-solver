import random
from time import sleep
from graphics import Cell, Window


class Maze:
    def __init__(
        self,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        win: Window | None = None,
        x1: int = 0,
        y1: int = 0,
        seed: int | None = None,
    ) -> None:
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells: list[list[Cell]] = []
        self.__maze_area = (num_rows * cell_size_y) * (num_cols * cell_size_x)
        if self.__win:
            self.__ani_factor: int = max(1, (num_rows * num_cols) // 100)
        if seed is not None:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)

    def get_cells(self) -> list[list[Cell]]:
        return self.__cells

    def _create_cells(self) -> None:
        if self.__num_cols <= 0 or self.__num_rows <= 0:
            raise ValueError("Maze dimensions must be greater than 0")
        for i in range(self.__num_cols):
            self.__cells.append([])
            for j in range(self.__num_rows):
                x1: int = i * self.__cell_size_x + self.__x1
                x2: int = x1 + self.__cell_size_x
                y1: int = j * self.__cell_size_y + self.__y1
                y2: int = y1 + self.__cell_size_y
                cell: Cell = Cell(x1, x2, y1, y2, self.__win)
                self._draw(cell)
                self.__cells[i].append(cell)

    def _draw(self, cell: Cell) -> None:
        self._animate()
        cell.draw()

    def _animate(self) -> None:
        if not self.__win:
            return
        cell_count: int = len(self.__cells[-1])
        if cell_count % self.__ani_factor == 0:
            self.__win.redraw()
            sleep(0.05)

    def _break_entrance_and_exit(self) -> None:
        self.__cells[0][0].has_top_wall = False
        self.__cells[0][0].draw()
        self.__cells[-1][-1].has_bottom_wall = False
        self.__cells[-1][-1].draw()

    def _break_walls_r(self, i: int, j: int) -> None:
        # Depth-first-search with backtracking
        self.__cells[i][j].visited = True
        while True:
            # Define cardinal directions with their indices
            directions = [
                ((i - 1, j), 0),  # N = 0
                ((i, j + 1), 1),  # E = 1
                ((i + 1, j), 2),  # S = 2
                ((i, j - 1), 3),  # W = 3
            ]
            to_visit: list[tuple[tuple[int, int], int]] = []
            # Valid directions to visit
            for (new_i, new_j), dir_idx in directions:
                if 0 <= new_i < self.__num_rows and 0 <= new_j < self.__num_cols:
                    if not self.__cells[new_i][new_j].visited:
                        to_visit.append(((new_i, new_j), dir_idx))
            if len(to_visit) == 0:
                self.__cells[i][j].draw()
                return

            # Choose random direction from available ones
            rand_idx: int = random.randrange(0, len(to_visit))
            visiting = to_visit[rand_idx]
            n_i, n_j = visiting[0]
            direction = visiting[1]
            self._break_wall(i, j, n_i, n_j, direction)
            self._break_walls_r(n_i, n_j)

    def _break_wall(
        self, from_i: int, from_j: int, to_i: int, to_j: int, direction: int
    ) -> None:
        # Break the appropriate walls based on direction
        if direction == 0:  # N
            self.__cells[from_i][from_j].has_top_wall = False
            self.__cells[to_i][to_j].has_bottom_wall = False
        elif direction == 1:  # E
            self.__cells[from_i][from_j].has_right_wall = False
            self.__cells[to_i][to_j].has_left_wall = False
        elif direction == 2:  # S
            self.__cells[from_i][from_j].has_bottom_wall = False
            self.__cells[to_i][to_j].has_top_wall = False
        elif direction == 3:  # W
            self.__cells[from_i][from_j].has_left_wall = False
            self.__cells[to_i][to_j].has_right_wall = False
        else:
            raise ValueError("Invalid cardinality index")

        # Draw both cells
        self.__cells[from_i][from_j].draw()
        self.__cells[to_i][to_j].draw()
