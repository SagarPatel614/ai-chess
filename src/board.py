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
        self.last_move = None
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

            # castling
            if not piece.moved:
                # queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            if self.squares[row][c].has_piece():
                                break  # castling not possible, sa there are pieces in between
                            if c == 3:
                                piece.left_rook = left_rook  # add left rook to king
                                # rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                move = Move(initial, final)
                                left_rook.add_move(move)
                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                move = Move(initial, final)
                                piece.add_move(move)

                # king castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            if self.squares[row][c].has_piece():
                                break  # castling not possible, sa there are pieces in between
                            if c == 6:
                                piece.right_rook = right_rook  # add right rook to king
                                # rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                move = Move(initial, final)
                                right_rook.add_move(move)
                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                move = Move(initial, final)
                                piece.add_move(move)

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        # console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # pawn promotion
        if isinstance(piece, Pawn):
            self.check_promotion(piece, final)

        # king castling
        if isinstance(piece, King):
            if self.castling(initial, final):
                dif = final.col = initial.col
                rook = piece.left_rook if (dif < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        # Piece moved
        piece.moved = True
        # clear valid moves
        piece.clear_moves()
        # update last move
        self.last_move = move

    @staticmethod
    def valid_move(piece, move):
        return move in piece.moves

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2
