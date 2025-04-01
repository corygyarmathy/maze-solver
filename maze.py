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
        self._reset_cells_visited()

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
            next_index_list: list[tuple[int, int]] = []

            # determine valid cell(s) to visit next
            # left
            if i > 0 and not self.__cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
            # right
            if i < self.__num_cols - 1 and not self.__cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
            # up
            if j > 0 and not self.__cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            # down
            if j < self.__num_rows - 1 and not self.__cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))

            # no valid cells, terminate loop
            if len(next_index_list) == 0:
                # Drawing when no valid cells creates animation
                self._draw(cell=self.__cells[i][j])
                return

            # randomly choose the next direction to go
            direction_index: int = random.randrange(0, len(next_index_list))
            next_index: tuple[int, int] = next_index_list[direction_index]

            # knock out walls between this cell and the next cell(s)
            # right
            if next_index[0] == i + 1:
                self.__cells[i][j].has_right_wall = False
                self.__cells[i + 1][j].has_left_wall = False
            # left
            if next_index[0] == i - 1:
                self.__cells[i][j].has_left_wall = False
                self.__cells[i - 1][j].has_right_wall = False
            # down
            if next_index[1] == j + 1:
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[i][j + 1].has_top_wall = False
            # up
            if next_index[1] == j - 1:
                self.__cells[i][j].has_top_wall = False
                self.__cells[i][j - 1].has_bottom_wall = False

            # recursively visit the next cell
            self._break_walls_r(i=next_index[0], j=next_index[1])

    def _reset_cells_visited(self) -> None:
        for col in self.__cells:
            for cell in col:
                cell.visited = False

    def solve(self) -> bool:
        solved = self._solve_r(0, 0)
        return solved

    def _solve_r(self, i: int = 0, j: int = 0) -> bool:
        self._animate()
        self.__cells[i][j].visited = True

        # Reached the end cell. Solved!
        if self.__cells[i][j] == self.__cells[-1][-1]:
            return True

        # determine valid cell(s) to move to next
        # left
        if i > 0 and not self.__cells[i - 1][j].visited:
            if not self.__cells[i][j].has_left_wall:
                self.__cells[i][j].draw_move(self.__cells[i - 1][j])
                if self._solve_r(i - 1, j):
                    return True
                self.__cells[i][j].draw_move(self.__cells[i - 1][j], True)
        # right
        if i < self.__num_cols - 1 and not self.__cells[i + 1][j].visited:
            if not self.__cells[i][j].has_right_wall:
                self.__cells[i][j].draw_move(self.__cells[i + 1][j])
                if self._solve_r(i + 1, j):
                    return True
                self.__cells[i][j].draw_move(self.__cells[i + 1][j], True)
        # up
        if j > 0 and not self.__cells[i][j - 1].visited:
            if not self.__cells[i][j].has_top_wall:
                self.__cells[i][j].draw_move(self.__cells[i][j - 1])
                if self._solve_r(i, j - 1):
                    return True
                self.__cells[i][j].draw_move(self.__cells[i][j - 1], True)
        # down
        if j < self.__num_rows - 1 and not self.__cells[i][j + 1].visited:
            if not self.__cells[i][j].has_bottom_wall:
                self.__cells[i][j].draw_move(self.__cells[i][j + 1])
                if self._solve_r(i, j + 1):
                    return True
                self.__cells[i][j].draw_move(self.__cells[i][j + 1], True)

        # Invalid path
        return False
