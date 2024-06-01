import copy
import os

from src.const import *
from src.sound import Sound
from src.square import Square
from src.piece import *
from src.move import Move


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

    def create_move(self, piece, row, col, p_row, p_col, final_piece=None, check=True):
        initial = Square(row, col)
        final = Square(p_row, p_col, final_piece)
        move = Move(initial, final)
        if check:
            if not self.in_check(piece, move):
                piece.add_move(move)
        else:
            piece.add_move(move)

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, in_check=True)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_rival_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, check_flag=False)  # We flag the calc method to eliminate loop
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        return False

    def calc_moves(self, piece: Piece, row: int, col: int, check_flag: bool = True):
        # Pawn moves
        if isinstance(piece, Pawn):
            vertical_moves, diagonal_moves = piece.valid_moves(row, col)
            # Vertical moves
            for v_move in vertical_moves:
                p_row, p_col = v_move
                if self.squares[p_row][p_col].is_empty():
                    self.create_move(piece, row, col, p_row, p_col, check=check_flag)
            # Diagonal moves
            for d_move in diagonal_moves:
                p_row, p_col = d_move
                if self.squares[p_row][p_col].has_rival_piece(piece.color):
                    final_piece = self.squares[p_row][p_col].piece
                    self.create_move(piece, row, col, p_row, p_col, final_piece, check=check_flag)

            # En passant
            r = 3 if piece.color == 'white' else 4
            fr = 2 if piece.color == 'white' else 5
            # Left en passant
            if in_range(col-1) and row == r:
                if self.squares[row][col-1].has_rival_piece(piece.color):
                    p = self.squares[row][col-1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            self.create_move(piece, row, col, fr, col-1, p, check_flag)
            # Right en passant
            if in_range(col+1) and row == r:
                if self.squares[row][col+1].has_rival_piece(piece.color):
                    p = self.squares[row][col+1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            self.create_move(piece, row, col, fr, col+1, p, check_flag)

        # Knight moves
        elif isinstance(piece, Knight):
            possible_moves = piece.valid_moves(row, col)
            for move in possible_moves:
                p_row, p_col = move
                if self.squares[p_row][p_col].is_empty_or_rival(piece.color):
                    final_piece = self.squares[p_row][p_col].piece
                    self.create_move(piece, row, col, p_row, p_col, final_piece, check=check_flag)
        # Bishop, Rook, Queen
        elif isinstance(piece, Bishop) or isinstance(piece, Rook) or isinstance(piece, Queen):
            directions = piece.directions

            for direction in directions:
                r, c = direction
                p_row, p_col = row + r, col + c

                while True:
                    if in_range(p_row, p_col):
                        initial = Square(row, col)
                        final_piece = self.squares[p_row][p_col].piece
                        final = Square(p_row, p_col, final_piece)
                        move = Move(initial, final)

                        if self.squares[p_row][p_col].is_empty():
                            if check_flag:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                        elif self.squares[p_row][p_col].has_rival_piece(piece.color):
                            if check_flag:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            break
                        elif self.squares[p_row][p_col].has_team_piece(piece.color):
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
                    self.create_move(piece, row, col, p_row, p_col, check=check_flag)

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
                                move_r = Move(initial, final)
                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                move_k = Move(initial, final)

                                if check_flag:
                                    if not self.in_check(piece, move_k) and not self.in_check(left_rook, move_r):
                                        piece.add_move(move_k)
                                        left_rook.add_move(move_r)
                                else:
                                    piece.add_move(move_k)
                                    left_rook.add_move(move_r)

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
                                move_r = Move(initial, final)
                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                move_k = Move(initial, final)

                                if check_flag:
                                    if not self.in_check(piece, move_k) and not self.in_check(right_rook, move_r):
                                        piece.add_move(move_k)
                                        right_rook.add_move(move_r)
                                else:
                                    piece.add_move(move_k)
                                    right_rook.add_move(move_r)

    def move(self, piece, move, in_check=False):
        initial = move.initial
        final = move.final

        en_passant_empty = self.squares[final.row][final.col].is_empty()

        # console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # pawn promotion
        if isinstance(piece, Pawn):
            diff = final.col - initial.col
            if diff != 0 and en_passant_empty:
                # console board move update
                self.squares[initial.row][initial.col + diff].piece = None
                if not in_check:
                    sound = Sound(os.path.join(
                        'assets/sounds/capture.wav'
                    ))
                    sound.play()
            # # pawn en passant
            # if self.en_passant(initial, final):
            #     piece.en_passant = True
            else:
                self.check_promotion(piece, final)  # pawn promotion

        # king castling
        if isinstance(piece, King):
            if self.castling(initial, final) and not in_check:
                dif = final.col - initial.col
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

    @staticmethod
    def castling(initial, final):
        return abs(initial.col - final.col) == 2

    @staticmethod
    def en_passant(initial, final):
        return abs(initial.row - final.row) == 2

    def reset_en_passant(self, piece):
        if not isinstance(piece, Pawn):
            return

        for row in range(ROWS):
            for col in range(COLS):
                p = self.squares[row][col].piece
                if isinstance(p, Pawn) and self.last_move.final.piece != p:
                    p.en_passant = False

        piece.en_passant = True
