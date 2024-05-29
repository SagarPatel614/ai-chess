from src.square import Square


class Move:
    def __init__(self, initial: Square, final: Square):
        # Initial and final squares
        self.initial = initial
        self.final = final
