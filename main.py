from graphics import Line, Point, Window


def main() -> None:
    win: Window = Window(800, 600)
    p1: Point = Point(300, 200)
    p2: Point = Point(100, 500)
    p3: Point = Point(500, 50)
    p4: Point = Point(200, 400)
    l1: Line = Line(p1, p2)
    l2: Line = Line(p3, p4)

    win.draw_line(l1, "black")
    win.draw_line(l2, "red")

    win.wait_for_close()


if __name__ == "__main__":
    _ = main()
