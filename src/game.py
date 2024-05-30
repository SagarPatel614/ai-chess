import pygame
from src.const import *
from src.board import Board
from src.dragger import Dragger
from src.piece import Piece


def render_piece(piece: Piece, surface: pygame.Surface, img_center: tuple[int, int]) -> None:
    img = pygame.image.load(piece.texture)
    piece.texture_rect = img.get_rect(center=img_center)
    surface.blit(img, piece.texture_rect)


class Game:
    def __init__(self):
        self.player = 'white'
        self.hovered_square = None
        self.board = Board()
        self.dragger = Dragger()

    # Show methods
    @staticmethod
    def show_bg(surface: pygame.Surface) -> None:
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (234, 235, 200)  # Light green
                else:
                    color = (119, 154, 88)  # dark green

                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_pieces(self, surface: pygame.Surface) -> None:
        for row in range(ROWS):
            for col in range(COLS):
                # piece ?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    # render all pieces except the moving one
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        render_piece(piece, surface, img_center)

    def show_moves(self, surface: pygame.Surface) -> None:
        if self.dragger.dragging:
            piece = self.dragger.piece
            # Loop over all moves
            for move in piece.moves:
                # create color
                color = '#C86464' if (move.final.row + move.final.col) % 2 == 0 else '#C84646'
                # create rect
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface: pygame.Surface) -> None:
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            for pos in [initial, final]:
                # color
                color = (244, 247, 116) if (pos.row + pos.col) % 2 == 0 else (172, 195, 51)
                # rect
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface: pygame.Surface) -> None:
        if self.hovered_square:
            # color
            color = (180, 180, 180)
            # rect
            rect = (self.hovered_square.col * SQSIZE, self.hovered_square.row * SQSIZE, SQSIZE, SQSIZE)
            # blit
            pygame.draw.rect(surface, color, rect, width=3)

    def next_turn(self) -> None:
        self.player = 'white' if self.player == 'black' else 'black'

    def set_hover(self, row: int, col: int) -> None:
        self.hovered_square = self.board.squares[row][col]
