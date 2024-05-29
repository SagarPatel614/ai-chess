
class Square:

    def __init__(self, row=0, col=0, piece=None):
        self.row = row
        self.col = col
        self.piece = piece

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
