from graphics import Cell, Line, Point, Window


def main() -> None:
    win: Window = Window(800, 600)

    c1: Cell = Cell(100, 200, 100, 200, win)
    c1.has_left_wall = False
    c1.draw()

    c2: Cell = Cell(200, 300, 200, 300, win)
    c2.has_right_wall = False
    c2.draw()

    c3: Cell = Cell(300, 400, 300, 400, win)
    c3.has_top_wall = False
    c3.draw()

    c4: Cell = Cell(400, 500, 400, 500, win)
    c4.has_bottom_wall = False
    c4.draw()

    win.wait_for_close()


if __name__ == "__main__":
    _ = main()
