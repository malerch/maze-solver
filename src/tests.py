import unittest

from maze import Maze
from priority_queue import PriorityQueue


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )

    def test_maze_create_square_cells(self):
        num_cols = 30
        num_rows = 30
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )

    def test_break_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1._Maze__break_entrance_and_exit()
        first_cell = m1._Maze__cells[0][0]
        last_cell = (
            m1._Maze__cells[len(m1._Maze__cells)-1][len(m1._Maze__cells[0])-1]
        )
        self.assertFalse(
            first_cell.has_top_wall
            or last_cell.has_bottom_wall
        )

    def test_reset_cells_visited(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1._Maze__cells[0][0].visited = True
        m1._Maze__reset_cells_visited()
        self.assertFalse(m1._Maze__cells[0][0].visited)

    def test_priority_queue_priority(self):
        queue = PriorityQueue()
        queue.push(10, (1, 0))
        queue.push(15, (2, 0))
        queue.push(20, (2, 0))
        self.assertEqual(queue.priority(0), 10)

if __name__ == "__main__":
    unittest.main()
