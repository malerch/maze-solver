from tkinter import BOTH, Canvas, Tk

from graphics import Cell, Line, Point, Window


def main():
    win = Window(800, 600)

    cell1 = Cell(win)

    cell2 = Cell(win)

    cell1.draw(50, 100, 50, 100)
    cell2.draw(100, 150, 50, 100)
    cell1.draw_move(cell2, True)

    win.wait_for_close()

if __name__ == "__main__":
    main()
