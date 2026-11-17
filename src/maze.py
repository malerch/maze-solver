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
    ) -> None:
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells = []
        self.__create_cells()

    def __create_cells(self):
        for i in range(self.__num_cols):
            self.__cells.append([])
            for j in range(self.__num_rows):
                self.__cells[i].append(Cell(self.__win))
                self.__draw_cell(i, j)
        self.__break_entrance_and_exit()

    def __draw_cell(self, i: int, j: int):
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
            time.sleep(0.05)

    def __break_entrance_and_exit(self) -> None:
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0)

        last_cell: Cell = (
            self.__cells[len(self.__cells) - 1][len(self.__cells[0]) - 1]
        )
        last_cell.has_bottom_wall = False
        self.__draw_cell(len(self.__cells) - 1, len(self.__cells[0]) - 1)
