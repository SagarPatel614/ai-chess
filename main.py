import sys

import pygame

from src.const import *
from src.game import Game
from src.square import Square
from src.move import Move


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
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

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
                        # Valid player piece
                        if piece.color == game.player:
                            board.calc_moves(piece, clicked_row, clicked_col, check_flag=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                            # show method
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                # Mouse Motion
                elif event.type == pygame.MOUSEMOTION:
                    m_row = event.pos[1] // SQSIZE
                    m_col = event.pos[0] // SQSIZE
                    game.set_hover(m_row, m_col)
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                # Mouse Release
                elif event.type == pygame.MOUSEBUTTONUP:
                    # Perform the move
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        release_row = dragger.mouseY // SQSIZE
                        release_col = dragger.mouseX // SQSIZE

                        # create initial move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(release_row, release_col)
                        move = Move(initial, final)

                        # Is this a valid move
                        if board.valid_move(dragger.piece, move):
                            # Normal Capture
                            captured = board.squares[release_row][release_col].has_piece()
                            # move the piece
                            board.move(dragger.piece, move)
                            board.reset_en_passant(dragger.piece)
                            # play sound
                            game.play_sound(captured)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            # change turn
                            game.next_turn()

                    dragger.undrag_piece()

                # Key Press
                elif event.type == pygame.KEYDOWN:
                    # Changing theme
                    if event.key == pygame.K_t:
                        game.change_theme()

                    # Game reset
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                # Game Quit
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update screen post input
            pygame.display.update()


main = Main()
main.mainloop()
