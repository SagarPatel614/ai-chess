from src.const import *
from src.square import Square


class Board:

    def __init__(self):
        self.square = [[0, 0, 0, 0, 0, 0, 0, 0] for _ in range(COLS)]

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.square[row][col] = Square(row, col)

    def _add_piece(self, color):
        pass
