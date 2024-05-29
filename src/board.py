from src.const import *
from src.square import Square
from src.piece import *
from src.move import Move


def create_move(piece, row, col, p_row, p_col):
    initial = Square(row, col)
    final = Square(p_row, p_col)  # piece=piece
    move = Move(initial, final)
    piece.add_move(move)


class Board:

    def __init__(self):
        self.squares = [[Square(0, 0) for _ in range(ROWS)] for _ in range(ROWS)]
        self._create()
        self._add_piece('white')
        self._add_piece('black')

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_piece(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)
        # Pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # Rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))
        # Knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))
        # Bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
        # Queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        # King
        self.squares[row_other][4] = Square(row_other, 4, King(color))

    def calc_moves(self, piece: Piece, row: int, col: int):
        # Pawn moves
        if isinstance(piece, Pawn):
            vertical_moves, diagonal_moves = piece.valid_moves(row, col)
            # Vertical moves
            for v_move in vertical_moves:
                p_row, p_col = v_move
                if self.squares[p_row][p_col].is_empty():
                    create_move(piece, row, col, p_row, p_col)
            # Diagonal moves
            for d_move in diagonal_moves:
                p_row, p_col = d_move
                if self.squares[p_row][p_col].has_rival_piece(piece.color):
                    create_move(piece, row, col, p_row, p_col)
        # Knight moves
        elif isinstance(piece, Knight):
            possible_moves = piece.valid_moves(row, col)
            for move in possible_moves:
                p_row, p_col = move
                if self.squares[p_row][p_col].is_empty_or_rival(piece.color):
                    create_move(piece, row, col, p_row, p_col)

        # Bishop, Rook, Queen
        elif isinstance(piece, Bishop) or isinstance(piece, Rook) or isinstance(piece, Queen):
            directions = piece.directions

            for direction in directions:
                r, c = direction
                p_row, p_col = row + r, col + c

                while True:
                    if in_range(p_row, p_col):
                        initial = Square(row, col)
                        final = Square(p_row, p_col)
                        move = Move(initial, final)

                        if self.squares[p_row][p_col].is_empty():
                            piece.add_move(move)
                        if self.squares[p_row][p_col].has_rival_piece(piece.color):
                            piece.add_move(move)
                            break
                        if self.squares[p_row][p_col].has_team_piece(piece.color):
                            break
                    else:
                        break

                    p_row, p_col = p_row + r, p_col + c

        # King
        elif isinstance(piece, King):
            possible_moves = piece.valid_moves(row, col)
            for move in possible_moves:
                p_row, p_col = move
                if self.squares[p_row][p_col].is_empty_or_rival(piece.color):
                    create_move(piece, row, col, p_row, p_col)
