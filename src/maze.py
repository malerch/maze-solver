import random
import time

from cell import Cell
from graphics import Window


class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: float,
        cell_size_y: float,
        win: Window | None = None,
        seed: int | None = None
    ) -> None:
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__seed = random.seed(seed) if seed is not None else None
        self.__cells = []
        self.__create_cells()

    def __create_cells(self):
        for i in range(self.__num_cols):
            self.__cells.append([])
            for j in range(self.__num_rows):
                self.__cells[i].append(Cell(self.__win))
                self.__draw_cell(i, j)
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)

    def __draw_cell(self, i: int, j: int):
        #time.sleep(0.05)
        x: float = self.__x1 + j * self.__cell_size_x
        y: float = self.__y1 + i * self.__cell_size_y
        self.__cells[i][j].draw(
            x,
            x + self.__cell_size_x,
            y,
            y + self.__cell_size_y
        )
        self.__animate()

    def __animate(self):
        if self.__win is not None:
            self.__win.redraw()
            #time.sleep(0.05)

    def __break_entrance_and_exit(self) -> None:
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0)
        self.__cells[self.__num_cols - 1][self.__num_rows - 1].has_bottom_wall = False
        self.__draw_cell(self.__num_cols - 1, self.__num_rows - 1)

    def __break_walls_r(self, i, j) -> None:
        current = self.__cells[i][j]
        current.visited = True

        while True:
            to_visit: list[tuple[int, int]] = []
            if i > 0 and not self.__cells[i - 1][j].visited:
                to_visit.append((i - 1, j))
            if i < self.__num_cols - 1 and not self.__cells[i + 1][j].visited:
                to_visit.append((i + 1, j))
            if j > 0 and not self.__cells[i][j - 1].visited:
                to_visit.append((i, j - 1))
            if j < self.__num_rows - 1 and not self.__cells[i][j + 1].visited:
                to_visit.append((i, j + 1))


            if len(to_visit) == 0:
                self.__draw_cell(i, j)
                return

            visiting = to_visit[random.randrange(len(to_visit))]
            next_neighbor = self.__cells[visiting[0]][visiting[1]]

            if visiting[1] > j:
                current.has_right_wall = False
                next_neighbor.has_left_wall = False
            elif visiting[1] < j:
                current.has_left_wall = False
                next_neighbor.has_right_wall = False
            elif visiting[0] < i:
                current.has_top_wall = False
                next_neighbor.has_bottom_wall = False
            elif visiting[0] > i:
                current.has_bottom_wall = False
                next_neighbor.has_top_wall = False

            self.__break_walls_r(visiting[0], visiting[1])
