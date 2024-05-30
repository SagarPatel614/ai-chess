import os
from typing import List, Tuple, Any


def in_range(*args) -> bool:
    return all(0 <= arg <= 7 for arg in args)


def straight_line_moves(directions, row, col):
    moves = [(row + r, col + c) for r, c in directions if in_range(row + r, col + c)]
    return moves


class Piece:

    def __init__(self, name: str, color: str, value: float, texture: str = None, texture_rect=None):
        self.name = name
        self.color = color
        value_sign = 1 if color == 'white' else -1
        self.value = value * value_sign
        self.moves = []
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self, size: int = 80) -> None:
        self.texture = os.path.join(
            f'assets/images/imgs-{size}px/{self.color}_{self.name}.png'
        )

    def add_move(self, move) -> None:
        self.moves.append(move)

    def _valid_moves(self, row: int, col: int) -> Any:
        return NotImplemented("The method needs to be implemented by the derived class!")

    def valid_moves(self, row: int, col: int) -> Any:
        return self._valid_moves(row, col)

    def clear_moves(self) -> None:
        self.moves = []


class Pawn(Piece):

    def __init__(self, color: str):
        self.dir = -1 if color == 'white' else 1
        super().__init__(name='pawn', color=color, value=1.0)

    def _valid_vertical_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        step = 1 if self.moved else 2
        # vertical moves
        start = row + self.dir
        end = row + (self.dir * (1 + step))
        moves = []
        for move_row in range(start, end, self.dir):
            if in_range(move_row):
                moves.append((move_row, col))

        return moves

    def _valid_moves(self, row, col) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        return self._valid_vertical_moves(row, col), self._valid_diagonal_moves(row, col)

    def _valid_diagonal_moves(self, row, col) -> List[Tuple[int, int]]:
        moves = []
        possible_move_row = row + self.dir
        possible_move_cols = [col - 1, col + 1]
        for p_col in possible_move_cols:
            if in_range(p_col):
                moves.append((possible_move_row, p_col))
        return moves


class Knight(Piece):

    def __init__(self, color: str):
        super().__init__(name='knight', color=color, value=3.0)

    def _valid_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        # 8 Possible moves
        possible_moves = [
            (row - 2, col + 1),
            (row - 1, col + 2),
            (row + 1, col + 2),
            (row + 2, col + 1),
            (row + 2, col - 1),
            (row + 1, col - 2),
            (row - 1, col - 2),
            (row - 2, col - 1),
        ]
        return [(p_row, p_col) for p_row, p_col in possible_moves if in_range(p_row, p_col)]


class Bishop(Piece):

    def __init__(self, color: str):
        self.directions = [(-1, 1), (-1, -1), (1, 1), (1, -1)]
        super().__init__(name='bishop', color=color, value=3.001)

    def _valid_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        return straight_line_moves(self.directions, row, col)


class Rook(Piece):

    def __init__(self, color: str):
        self.directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        super().__init__(name='rook', color=color, value=5.0)

    def _valid_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        return straight_line_moves(self.directions, row, col)


class Queen(Piece):

    def __init__(self, color: str):
        self.directions = [(-1, 1), (-1, -1), (1, 1), (1, -1), (-1, 0), (1, 0), (0, 1), (0, -1)]
        super().__init__(name='queen', color=color, value=9.0)

    def _valid_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        return straight_line_moves(self.directions, row, col)


class King(Piece):

    def __init__(self, color: str):
        self.left_rook = None
        self.right_rook = None
        super().__init__(name='king', color=color, value=10000.0)

    def _valid_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        # 8 Possible moves
        possible_moves = [
            (row - 1, col),
            (row + 1, col),
            (row - 1, col - 1),
            (row - 1, col + 1),
            (row + 1, col - 1),
            (row + 1, col + 1),
            (row, col - 1),
            (row, col + 1),
        ]
        return [(p_row, p_col) for p_row, p_col in possible_moves if in_range(p_row, p_col)]
