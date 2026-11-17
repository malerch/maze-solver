from cell import Cell
from graphics import Line, Point, Window
from maze import Maze


def main():
    win = Window(800, 600)

    maze = Maze(25, 25, 10, 9, 50, 50, win)

    win.wait_for_close()

if __name__ == "__main__":
    main()
