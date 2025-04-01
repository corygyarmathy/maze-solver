import unittest

from maze import Maze


class TestClass(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1: Maze = Maze(num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1.get_cells()),
            num_cols,
        )
        self.assertEqual(
            len(m1.get_cells()[0]),
            num_rows,
        )

    def test_maze_create_cells_large(self):
        num_cols = 20
        num_rows = 20
        m1: Maze = Maze(num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1.get_cells()),
            num_cols,
        )
        self.assertEqual(
            len(m1.get_cells()[0]),
            num_rows,
        )

    def test_maze_entrance_exit(self):
        num_cols = 12
        num_rows = 10
        m1: Maze = Maze(num_rows, num_cols, 10, 10)
        self.assertEqual(m1.get_cells()[0][0].has_top_wall, False)
        self.assertEqual(m1.get_cells()[-1][-1].has_bottom_wall, False)

    def test_maze_reset_cells_visited(self):
        num_cols = 12
        num_rows = 10
        m1: Maze = Maze(num_rows, num_cols, 10, 10)
        for col in m1.get_cells():
            for cell in col:
                self.assertEqual(
                    cell.visited,
                    False,
                )


if __name__ == "__main__":
    _ = unittest.main()
