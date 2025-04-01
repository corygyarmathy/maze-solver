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
        self._create_cells()

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
        if self.__win:
            cell_count: int = len(self.__cells[-1])
            if cell_count % self.__ani_factor == 0:
                self.__win.redraw()
                sleep(0.05)

    def get_cells(self) -> list[list[Cell]]:
        return self.__cells
