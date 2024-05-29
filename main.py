import sys

import pygame

from src.const import *
from src.game import Game


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):
        game = self.game
        screen = self.screen
        board = self.game.board
        dragger = self.game.dragger

        while True:
            # Game display
            game.show_bg(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            # Display moving piece
            if dragger.dragging:
                dragger.update_blit(screen)

            # Game controls
            for event in pygame.event.get():
                # Mouse Click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    clicked_row, clicked_col = dragger.calc_position(event.pos)

                    # If clicked square has a piece
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        board.calc_moves(piece, clicked_row, clicked_col)
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(piece)

                        # show method
                        game.show_bg(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)

                # Mouse Motion
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)

                # Mouse Release
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragger.undrag_piece()

                # Game Quit
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update screen post input
            pygame.display.update()


main = Main()
main.mainloop()
