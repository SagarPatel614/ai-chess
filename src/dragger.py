import pygame

from src.const import *
from src.piece import Piece


class Dragger:

    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0

    def update_mouse(self, pos: tuple[int, int]) -> None:
        self.mouseX, self.mouseY = pos  # (xCor, yCor)

    def save_initial(self, pos: tuple[int, int]) -> None:
        self.initial_row, self.initial_col = self.calc_position(pos)

    @staticmethod
    def calc_position(pos: tuple[int, int]) -> tuple[int, int]:
        row = pos[1] // SQSIZE
        col = pos[0] // SQSIZE
        return row, col

    def drag_piece(self, piece: Piece) -> None:
        self.piece = piece
        self.dragging = True

    def undrag_piece(self) -> None:
        self.piece = None
        self.dragging = False

    def update_blit(self, surface: pygame.Surface) -> None:
        # Update texture
        self.piece.set_texture(size=128)
        texture = self.piece.texture
        # Image
        img = pygame.image.load(texture)
        # Rectangle
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center=img_center)
        surface.blit(img, self.piece.texture_rect)
