from graphics import BOTH, Tk, Canvas


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
