from graphics import Cell, Line, Point, Window
from maze import Maze


def main() -> None:
    num_rows = 120
    num_cols = 16
    margin = 50
    screen_x = 800
    screen_y = 600
    cell_size_x = 5
    cell_size_y = 4
    win = Window(screen_x, screen_y)

    maze = Maze(num_rows, num_cols, cell_size_x, cell_size_y, win, margin, margin)
    if maze.solve():
        print("Maze solved!")
    else:
        print("Maze could not be solved!")

    win.wait_for_close()


if __name__ == "__main__":
    _ = main()
