#!/usr/bin/python3
import numpy as np
import pygame
import sys
import math
from enums.colors import Colors
from enums.player import PLAYER


class ConnectPyGame:
    def __init__(self, number_of_rows=6, number_of_cols=7):
        pygame.init()
        self.NUM_ROWS = number_of_rows
        self.NUM_COLS = number_of_cols
        self.OFFSET = 200
        self.SQUARE_SIZE = 100
        self.WIDTH = self.NUM_COLS * self.SQUARE_SIZE
        self.HEIGHT = self.NUM_ROWS * self.SQUARE_SIZE + int(self.OFFSET)
        self.RADIUS = int(self.SQUARE_SIZE/2 - 5)
        self.screen = self.set_screen()
        self.font = pygame.font.SysFont("Comic Sans MS", int(self.OFFSET/4))

    def create_game_board(self):
        """
        Returns game board as np array

        Returns:
        - board (np.ndarray): Numpy array represents game board with size
            NUM_ROWS X NUM_COLS
        """
        return np.zeros((self.NUM_ROWS, self.NUM_COLS))

    def set_screen(self):
        """
        Set screen with size WIDTH x HEIGHT
        """
        return pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def update_pygame(self):
        """
        Update game display after some changes on pygame object
        """
        pygame.display.update()

    def draw_board(self, board):
        """
        Draw board from 2D numpy array
        """        
        # Draw main board
        pygame.draw.rect(self.screen,
                         Colors.BLUE.value,
                         (
                            0,
                            self.OFFSET,
                            self.WIDTH,
                            self.HEIGHT
                         ))
    
        for c in range(self.NUM_COLS):
            for r in range(self.NUM_ROWS):
                # Draw stones
                player_color = Colors.BLACK.value

                if board[r][c] == PLAYER.FIRST.value:
                    player_color = Colors.RED.value

                elif board[r][c] == PLAYER.SECOND.value:
                    player_color = Colors.YELLOW.value

                posx = int(c*self.SQUARE_SIZE + self.SQUARE_SIZE/2)
                posy = int(r*self.SQUARE_SIZE + self.SQUARE_SIZE/2 + self.OFFSET)

                pygame.draw.circle(self.screen,
                                   player_color,
                                   (posx,posy),
                                   self.RADIUS)

        self.update_pygame()

    def move(self, player, positions):
        # Reference position
        pos_x, pos_y = positions
        player = PLAYER.NONE
        color = Colors.BLACK.value
        if player is PLAYER.FIRST:
            color = Colors.RED.value
        elif player is PLAYER.SECOND:
            color = Colors.YELLOW.value
        pygame.draw.circle(self.screen, color,
                           (pos_x, pos_y), self.RADIUS)

    def move_mouse(self, posx, player_turn):
        pygame.draw.rect(self.screen, Colors.BLACK.value,
                         (0, int(self.OFFSET/2), self.WIDTH, self.SQUARE_SIZE))
        color = Colors.BLACK.value
        if player_turn is PLAYER.FIRST:
            color = Colors.RED.value
        elif player_turn is PLAYER.SECOND:
            color = Colors.YELLOW.value
        
        posy = int(self.OFFSET/2)+int(self.SQUARE_SIZE/2)

        pygame.draw.circle(self.screen, color,
                           (posx, posy), self.RADIUS)

    def place_stone(self, board, posx, player_turn):
        pygame.draw.rect(self.screen, Colors.BLACK.value,
                         (0, 0, self.WIDTH, self.SQUARE_SIZE))
        player_value = player_turn.value
        col = int(math.floor(posx / self.SQUARE_SIZE))
        row, is_row_found = self.get_row(board, col)
        if is_row_found :
            board = self.set_position(board, [row, col], player_value)
        else:
            print("No row is left to play in that column !")
        return board, is_row_found

    def flip_players(self, turn):
        if turn is PLAYER.FIRST:
            return PLAYER.SECOND
        elif turn is PLAYER.SECOND:
            return PLAYER.FIRST

    def get_row(self, board, col):
        is_row_found = False
        row_selected = None
        for r in reversed(range(self.NUM_ROWS)):
            if board[r][col] == 0:
                row_selected = r
                is_row_found = True
                break

        return row_selected, is_row_found

    def set_position(self, board, position, piece):
        """
        Set position of a stone on the board
        """
        row, col = position
        board[row][col] = piece
        return board

    def get_player_by_move(self, move):
        if move == PLAYER.FIRST.value:
            return PLAYER.FIRST
        elif move == PLAYER.SECOND.value:
            return PLAYER.SECOND
        else:
            return PLAYER.NONE

    def check_win(self, board):
        is_game_won, player = self.check_win_vertical(board)
        if is_game_won:
            print("PLAYER : {0} is WON! (vertical check)".format(player))
            return True, player

        is_game_won, player = self.check_win_horizontal(board)
        if is_game_won:
            print("PLAYER : {0} is WON! (horizontal check)".format(player))
            return True, player

        is_game_won, player = self.check_win_diagonal_pos(board)
        if is_game_won:
            print("PLAYER : {0} is WON! (diagonal pos check)".format(player))
            return True, player

        is_game_won, player = self.check_win_diagonal_neg(board)
        if is_game_won:
            print("PLAYER : {0} is WON! (diagonal neg check)".format(player))
            return True, player

        else:
            return False, PLAYER.NONE

    def check_win_horizontal(self, board):
        is_game_won = False
        player = PLAYER.NONE
        for r in reversed(range(self.NUM_ROWS)):
            row = board[r,:]
            for x in range(len(row)-4+1):
                elements = row[x:4+x]
                if elements[0] != 0:
                    counted = np.count_nonzero(elements == elements[0])
                    if counted == 4:
                        player = self.get_player_by_move(elements[0])
                        is_game_won = True
                        break

        return is_game_won, player

    def check_win_vertical(self, board):
        is_game_won = False
        player = PLAYER.NONE
        for col in reversed(range(self.NUM_COLS)):
            column = board[:,col]
            for x in range(len(column)-4+1):
                elements = column[x:4+x]
                if elements[0] != 0:
                    counted = np.count_nonzero(elements == elements[0])
                    if counted == 4:
                        player = self.get_player_by_move(elements[0])
                        is_game_won = True
                        break

        return is_game_won, player

    def check_win_diagonal_pos(self, board):
        is_game_won = False
        player = PLAYER.NONE
        for r in np.arange(self.NUM_ROWS-1,self.NUM_ROWS-4,-1):
            for c in np.arange(0,self.NUM_COLS-3-1,1):
                first_element = board[r,c]
                if first_element != 0:
                    if first_element == board[r-1,c+1] and \
                        first_element == board[r-2,c+2] and \
                            first_element == board[r-3,c+3]:
                            is_game_won = True
                            player = self.get_player_by_move(first_element)
                            break

        return is_game_won, player

    def check_win_diagonal_neg(self, board):
        is_game_won = False
        player = PLAYER.NONE
        for r in np.arange(0,self.NUM_ROWS-3,1):
            for c in np.arange(0,self.NUM_COLS-3-1,1):
                first_element = board[r,c]
                if first_element != 0:
                    if first_element == board[r+1,c+1] and \
                        first_element == board[r+2,c+2] and \
                            first_element == board[r+3,c+3]:
                            is_game_won = True
                            player = self.get_player_by_move(first_element)
                            break
        return is_game_won, player

    def check_draw(self, board):
        if np.all((board == 0)) is False:
            is_any_place_left = 0 in board
            return is_any_place_left
        else:
            return False
            
    def print_to_board(self, text, color):
        text_surface = self.font.render(text, False, color)
        self.screen.blit(text_surface, (0, 0))

    def run(self):
        game_over = False
        turn = PLAYER.FIRST
        board = self.create_game_board()
        self.update_pygame()

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                else:
                    text_turn = 'TURN : {0}'.format(self.get_player_by_move(turn.value)) 
                    self.print_to_board(text_turn,Colors.PURPLE.value)

                    # Draw a black circle where the mouse is located in x axis
                    if event.type == pygame.MOUSEMOTION:
                        self.move_mouse(event.pos[0], turn)

                    # Draw placed stone if the stone is placed somewhere eligible
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        board, is_row_found = self.place_stone(board, event.pos[0], turn)
                        # Only flip players when there is left any place to move ! 
                        if is_row_found:
                            turn = self.flip_players(turn)

                        # Check if the move is the winning move
                        is_player_won, player = self.check_win(board)
                        if is_player_won:
                            won_msg = '{0} PLAYER IS WON!'.format(player.name)
                            self.print_to_board(text=won_msg, color=Colors.GREEN.value)
                            self.draw_board(board)
                            pygame.time.wait(3000)
                            sys.exit()

                        # Check if the move is the winning move
                        is_draw = self.check_draw(board)
                        if is_draw:
                            self.print_to_board('DRAW!',color=Colors.YELLOW.value)
                            self.draw_board(board)
                            pygame.time.wait(3000)
                            sys.exit()

                self.draw_board(board)

if __name__ == "__main__":
    connect_two_game = ConnectPyGame(6,7)
    connect_two_game.run()
