import pygame
from src.const import *
from src.board import Board
from src.dragger import Dragger
from src.piece import Piece
from src.config import Config


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
        self.config = Config()
        self.theme = self.config.theme

    # Show methods
    def show_bg(self, surface: pygame.Surface) -> None:
        for row in range(ROWS):
            for col in range(COLS):
                color = self.theme.bg.light if (row + col) % 2 == 0 else self.theme.bg.dark
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
                color = self.theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else self.theme.moves.dark
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
                color = self.theme.trace.light if (pos.row + pos.col) % 2 == 0 else self.theme.trace.dark
                # rect
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface: pygame.Surface) -> None:
        if self.hovered_square:
            # color
            color = self.theme.hover
            # rect
            rect = (self.hovered_square.col * SQSIZE, self.hovered_square.row * SQSIZE, SQSIZE, SQSIZE)
            # blit
            pygame.draw.rect(surface, color, rect, width=3)

    def next_turn(self) -> None:
        self.player = 'white' if self.player == 'black' else 'black'

    def set_hover(self, row: int, col: int) -> None:
        self.hovered_square = self.board.squares[row][col]

    def change_theme(self) -> None:
        self.config.change_theme()
        self.theme = self.config.theme
