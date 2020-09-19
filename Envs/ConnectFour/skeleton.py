#!/usr/bin/python3
import numpy as np
import sys
import math
from enums.player import PLAYER

class ConnectFourEnv:
    def __init__(self, number_of_rows=6, number_of_cols=7):
        self.__NUM_ROWS = number_of_rows
        self.__NUM_COLS = number_of_cols
        self.state_dim = self.__NUM_ROWS * self.__NUM_COLS
        self.action_dim = 1

    def create_game_board(self):
        """
        Returns game board as np array

        Returns:
        - board (np.ndarray): Numpy array represents game board with size
            __NUM_ROWS X __NUM_COLS
        """
        return np.zeros((self.__NUM_ROWS, self.__NUM_COLS))


    def place_stone(self, board, posx, player_turn):
        player_value = player_turn.value
        # col = int(math.floor(posx / self.SQUARE_SIZE))
        # board = self.set_position(board, [row, col], player_value)
        return board

    def flip_players(self, turn):
        if turn is PLAYER.FIRST:
            return PLAYER.SECOND
        elif turn is PLAYER.SECOND:
            return PLAYER.FIRST

    def get_row(self, board, col):
        row_selected = None
        for r in reversed(range(self.__NUM_ROWS)):
            if board[r][col] == 0:
                row_selected = r
                break
        return row_selected

    def get_player_by_move(self, move):
        if move == PLAYER.FIRST.value:
            return PLAYER.FIRST
        elif move == PLAYER.SECOND.value:
            return PLAYER.SECOND
        else:
            return PLAYER.NONE

    def set_position(self, board, position, piece):
        """
        Set position of a stone on the board
        """
        row, col = position
        board[row][col] = piece
        return board

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
        for r in reversed(range(self.__NUM_ROWS)):
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
        for col in reversed(range(self.__NUM_COLS)):
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
        for r in np.arange(self.__NUM_ROWS-1,self.__NUM_ROWS-4,-1):
            for c in np.arange(0,self.__NUM_COLS-3-1,1):
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
        for r in np.arange(0,self.__NUM_ROWS-3,1):
            for c in np.arange(0,self.__NUM_COLS-3-1,1):
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

    def is_action_valid(self, action):
        """
        Check if the action lies in the action space
        """
        pass

    def print_to_board(self, text):
        pass

    def step(self, action):
        if self.is_action_valid(action):
            # PLACE GOD DAMN STONE
            pass
        else:
            # ABORT GAME
            pass

    def reset(self):
        return self.create_game_board()
    
