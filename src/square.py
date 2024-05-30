# Column letter map
ALPHACOLS = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}


class Square:

    def __init__(self, row=0, col=0, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        self.alphacol = ALPHACOLS[col]

    def __eq__(self, other) -> bool:
        return self.row == other.row and self.col == other.col

    def has_piece(self) -> bool:
        return self.piece is not None

    def is_empty(self) -> bool:
        return not self.has_piece()

    def has_team_piece(self, color: str) -> bool:
        return self.has_piece() and self.piece.color == color

    def has_rival_piece(self, color: str) -> bool:
        return self.has_piece() and self.piece.color != color

    def is_empty_or_rival(self, color: str) -> bool:
        return self.is_empty() or self.has_rival_piece(color)

    @staticmethod
    def get_alphacol(col: int) -> str:
        return ALPHACOLS[col]
