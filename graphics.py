from tkinter import BOTH, Tk, Canvas
from typing import Self


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y


class Line:
    def __init__(self, p1: Point, p2: Point) -> None:
        self.__p1 = p1
        self.__p2 = p2

    def draw(self, canvas: Canvas, fill_colour: str = "black") -> None:
        _ = canvas.create_line(
            self.__p1.x,
            self.__p1.y,
            self.__p2.x,
            self.__p2.y,
            fill=fill_colour,
            width=2,
        )


class Window:
    def __init__(self, width: int, height: int) -> None:
        self.__root: Tk = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas: Canvas = Canvas(
            master=self.__root, bg="white", height=height, width=width
        )
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running: bool = False
        self.__width: int = width
        self.__height: int = height

    def redraw(self) -> None:
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self) -> None:
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self) -> None:
        self.__running = False

    def draw_line(self, line: Line, fill_colour: str = "black") -> None:
        line.draw(self.__canvas, fill_colour)

    def get_width(self) -> int:
        self.__root.update_idletasks()
        return self.__canvas.winfo_width()

    def get_height(self) -> int:
        self.__root.update_idletasks()
        return self.__canvas.winfo_height()

    def get_area(self) -> int:
        return self.get_width() * self.get_height()


class Cell:
    def __init__(
        self,
        x1: int,
        x2: int,
        y1: int,
        y2: int,
        win: Window | None = None,
        has_left_wall: bool = True,
        has_right_wall: bool = True,
        has_top_wall: bool = True,
        has_bottom_wall: bool = True,
        fill_colour: str = "black",
    ) -> None:
        self.has_left_wall: bool = has_left_wall
        self.has_right_wall: bool = has_right_wall
        self.has_top_wall: bool = has_top_wall
        self.has_bottom_wall: bool = has_bottom_wall
        self._x1: int = x1
        self._x2: int = x2
        self._y1: int = y1
        self._y2: int = y2
        self.__win: Window | None = win
        self.fill_colour: str = fill_colour
        self.visited: bool = False

    def get_centre_x(self) -> int:
        return (self._x1 + self._x2) // 2

    def get_centre_y(self) -> int:
        return (self._y1 + self._y2) // 2

    def draw(self) -> None:
        lines: list[Line] = []
        lines.append(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)))
        lines.append(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)))
        lines.append(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)))
        lines.append(Line(Point(self._x1, self._y2), Point(self._x2, self._y2)))
        colours: list[str] = [self.fill_colour for _ in range(len(lines))]

        if not self.has_left_wall:
            colours[0] = "white"
        if not self.has_right_wall:
            colours[1] = "white"
        if not self.has_top_wall:
            colours[2] = "white"
        if not self.has_bottom_wall:
            colours[3] = "white"
        if self.__win:
            for i in range(len(lines)):
                self.__win.draw_line(lines[i], colours[i])

    def draw_move(self, to_cell: Self, undo: bool = False) -> None:
        fill_colour: str = "gray" if undo else "red"

        x1: int = self.get_centre_x()
        y1: int = self.get_centre_y()
        x2: int = to_cell.get_centre_x()
        y2: int = to_cell.get_centre_y()

        line: Line = Line(Point(x1, y1), Point(x2, y2))
        if self.__win:
            self.__win.draw_line(line, fill_colour)

    # def move(self, x1: int, x2: int, y1: int, y2: int) -> None:
    #     pass
