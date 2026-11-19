from graphics import Line, Point, Window

WHITE: str = "#dadada"


class Cell:
    def __init__(self, win: Window | None = None) -> None:
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1.0
        self.__x2 = -1.0
        self.__y1 = -1.0
        self.__y2 = -1.0
        self.__win = win
        self.visited = False

    def draw(self, x1: float, x2: float, y1: float, y2: float) -> None:
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2
        if self.__win is not None:
            left_wall = Line(Point(x1, y1), Point(x1, y2))
            left_color: str = "black" if self.has_left_wall else WHITE
            self.__win.draw_line(left_wall, left_color)

            top_wall = Line(Point(x1, y1), Point(x2, y1))
            top_color: str = "black" if self.has_top_wall else WHITE
            self.__win.draw_line(top_wall, top_color)

            right_wall = Line(Point(x2, y1), Point(x2, y2))
            right_color: str = "black" if self.has_right_wall else WHITE
            self.__win.draw_line(right_wall, right_color)

            bottom_wall = Line(Point(x1, y2), Point(x2, y2))
            bottom_color: str = "black" if self.has_bottom_wall else WHITE
            self.__win.draw_line(bottom_wall, bottom_color)

    def draw_move(self, to_cell: "Cell", undo: bool = False) -> None:
        color = "gray" if undo else "red"
        line = Line(
            Point(
                (self.__x1 + self.__x2) / 2,
                (self.__y1 + self.__y2) / 2
            ),
            Point(
                (to_cell.__x1 + to_cell.__x2) / 2,
                (to_cell.__y1 + to_cell.__y2) / 2
            )
        )
        if self.__win is not None:
            self.__win.draw_line(line, color)
