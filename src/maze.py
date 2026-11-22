import random
import time

from cell import Cell
from graphics import Window
from priority_queue import PriorityQueue


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
        self.__reset_cells_visited()

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

    def __reset_cells_visited(self) -> None:
        for row in self.__cells:
            for cell in row:
                if cell.visited:
                    cell.visited = False

    def __get_neighbors(self, i, j) -> list[tuple[int, int]]:
        neighbors: list[tuple[int, int]] = []
        current: Cell = self.__cells[i][j]
        if (
            i > 0 #and not self.__cells[i - 1][j].visited
            and not self.__cells[i - 1][j].has_bottom_wall
            and not current.has_top_wall
        ):
            neighbors.append((i - 1, j))
        if (
            i < self.__num_cols - 1 #and not self.__cells[i + 1][j].visited
            and not self.__cells[i + 1][j].has_top_wall
            and not current.has_bottom_wall
        ):
            neighbors.append((i + 1, j))
        if (
            j > 0 #and not self.__cells[i][j - 1].visited
            and not self.__cells[i][j - 1].has_right_wall
            and not current.has_left_wall
        ):
            neighbors.append((i, j - 1))
        if (
            j < self.__num_rows - 1 #and not self.__cells[i][j + 1].visited
            and not self.__cells[i][j + 1].has_left_wall
            and not current.has_right_wall
        ):
            neighbors.append((i, j + 1))

        return neighbors

    def solve(self) -> bool:
        return self.__BFS_solve_r(0, 0)

    # Return true if the current cell is an end cell OR it leads to the end cell
    # False if the current cell is a loser cell
    def __DFS_solve_r(self, i: int, j: int) -> bool:
        self.__animate()

        current: Cell = self.__cells[i][j]
        current.visited = True;

        if i == (self.__num_cols - 1) and (j == self.__num_rows - 1):
            print("End reached!")
            return True

        neighbors: list[tuple[int, int]] = self.__get_neighbors(i, j)

        for next_i, next_j in neighbors:
            next: Cell = self.__cells[next_i][next_j]
            if next.visited:
                continue
            current.draw_move(self.__cells[next_i][next_j], undo=False)
            #time.sleep(0.025)
            if self.__DFS_solve_r(next_i, next_j):
                return True
            else:
                current.draw_move(self.__cells[next_i][next_j], undo=True)
                #time.sleep(0.1)

        return False

    def __backtrack(self, current: tuple[int, int]) -> None:
        i, j = current[0], current[1]

        while len(self.__get_neighbors(i, j)) == 1:
            current_cell = self.__cells[i][j]
            prev_neighbor = self.__get_neighbors(i, j)[0]
            prev_neighbor_cell = self.__cells[prev_neighbor[0]][prev_neighbor[1]]

            current_cell.draw_move(prev_neighbor_cell, undo=True)
            self.__animate()

            i, j = prev_neighbor

    def __BFS_solve_r(self, i, j) -> bool:
        self.__animate()

        current: Cell = self.__cells[i][j]
        to_visit = [(0, 0)]
        predecessors: dict[Cell, Cell | None] = {current: None}

        while to_visit:
            i, j = to_visit.pop(0)
            next = self.__cells[i][j]
            draw_from = current
            neighbors = self.__get_neighbors(i, j)

            self.__cells[i][j].visited = True
            if not list(filter(
                lambda neighbor:
                    not self.__cells[neighbor[0]][neighbor[1]].visited,
                neighbors
            )):
                # Backtrack to last intersection
                self.__backtrack((i, j))


            for neighbor in neighbors:
                if (
                    not self.__cells[neighbor[0]][neighbor[1]].visited
                    and neighbor not in to_visit
                ):
                    to_visit.append(neighbor)
                else:
                    draw_from = self.__cells[neighbor[0]][neighbor[1]]
                    draw_from.draw_move(next, undo=False)
                    self.__animate()

            current = next
            if i == (self.__num_cols - 1) and (j == self.__num_rows - 1):
                return True

        return False
        """for next_i, next_j in to_visit:
            current.draw_move(self.__cells[next_i][next_j], undo=False)
            time.sleep(0.025)
        for next_i, next_j in to_visit:
            if self.__BFS_solve_r(next_i, next_j):
                return True
            else:
                current.draw_move(self.__cells[next_i][next_j], undo=True)
                time.sleep(0.1)"""

        return False

    def __cost(self, next: tuple[int, int], cost_so_far: int) -> int:
        return (cost_so_far + 1 + abs(next[0] - self.__num_cols - 1)
            + abs(next[-1] - self.__num_rows - 1))

    def __a_star_solve_r(self, i, j, cost_so_far: int = 0) -> bool:
        self.__animate()

        current: Cell = self.__cells[i][j]
        current.visited = True;
        queue: PriorityQueue = PriorityQueue()

        if i == (self.__num_cols - 1) and (j == self.__num_rows - 1):
            print("End reached!")
            return True

        neighbors: list[tuple[int, int]] = self.__get_neighbors(i, j)

        for neighbor in neighbors:
            if not self.__cells[neighbor[0]][neighbor[1]].visited:
                cost = self.__cost(neighbor, cost_so_far)
                queue.push(cost, neighbor)

        while not queue.empty():
            next_cost = queue.priority(0)
            next: tuple[int, int] | None = queue.pop()
            if next is None:
                continue
            current.draw_move(self.__cells[next[0]][next[1]], undo=False)
            #time.sleep(0.025)

            if self.__a_star_solve_r(next[0], next[1], next_cost):
                return True
            else:
                current.draw_move(self.__cells[next[0]][next[1]], undo=True)
                #time.sleep(0.1)

        return False
