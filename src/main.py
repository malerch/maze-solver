from cell import Cell
from graphics import Line, Point, Window
from maze import Maze


def main():
    win = Window(800, 600)

    #while True:
    maze = Maze(50, 50, 40, 40, 15, 15, win)
    maze.solve()

    win.wait_for_close()

if __name__ == "__main__":
    main()
