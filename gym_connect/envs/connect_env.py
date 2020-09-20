#!/usr/bin/python3

import numpy as np
import sys
import math

import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym_connect.envs.enums.colors import Colors
from gym_connect.envs.enums.player import PLAYER
from gym_connect.envs.enums.run_mode import MODE, PLAY_MODE
from gym_connect.envs.enums.results_enum import RESULTS

class ConnectEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, 
                number_of_rows=6, number_of_cols=7,
                game_mode=MODE.TERMINAL_DEBUG, 
                play_mode = PLAY_MODE.HUMAN_VS_HUMAN):
        self.__NUM_ROWS = number_of_rows
        self.__NUM_COLS = number_of_cols
        self.__mode_game = game_mode
        self.__mode_play = play_mode
        self.__state = self.create_game_board()
        self.__PLAYER = PLAYER.FIRST
        self.state_dim = self.__NUM_ROWS * self.__NUM_COLS
        self.action_dim = 1

    def __place_stone(self, column):
        is_row_found = False
        row, is_row_found = self.__get_row(column)
        if is_row_found:
            self.__set_position(row, column, self.__PLAYER.value)
        return is_row_found

    def __flip_players(self):
        if self.__PLAYER is PLAYER.FIRST:
            self.__PLAYER = PLAYER.SECOND
        elif self.__PLAYER is PLAYER.SECOND:
            self.__PLAYER = PLAYER.FIRST

    def __get_row(self, column):
        is_row_found = False
        row_selected = None
        for row in reversed(range(self.__NUM_ROWS)):
            if self.__state[row][column] == 0:
                row_selected = row
                is_row_found = True
                break
        return row_selected, is_row_found

    def __evaulate_action_result(self, player, game_result):
        is_done = False
        reward = -1
        if game_result is RESULTS.WON:
            is_done = True
            reward = 1
        elif game_result is RESULTS.DRAW:
            is_done = True
            reward = -1
        state = self.make_state(player)

        return state, is_done, reward

    def __set_position(self, row, col, piece):
        """
        Set position of a stone on the board
        """
        self.__state[row][col] = piece

    def __check_win(self):
        board = self.__state
        is_game_won, player = self.__check_win_vertical(board)
        if is_game_won:
            print("PLAYER : {0} is WON! (vertical check)".format(player))
            return RESULTS.WON, player

        is_game_won, player = self.__check_win_horizontal(board)
        if is_game_won:
            print("PLAYER : {0} is WON! (horizontal check)".format(player))
            return RESULTS.WON, player

        is_game_won, player = self.__check_win_diagonal_pos(board)
        if is_game_won:
            print("PLAYER : {0} is WON! (diagonal pos check)".format(player))
            return RESULTS.WON, player

        is_game_won, player = self.__check_win_diagonal_neg(board)
        if is_game_won:
            print("PLAYER : {0} is WON! (diagonal neg check)".format(player))
            return RESULTS.WON, player

        is_game_draw = self.__check_draw()
        if is_game_draw:
            print("PLAYER : {0} is WON! (diagonal neg check)".format(player))
            return RESULTS.DRAW, PLAYER.NONE

        else:
            return RESULTS.NOT_FINISHED, PLAYER.NONE

    def __check_win_horizontal(self, board):
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

    def __check_win_vertical(self, board):
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

    def __check_win_diagonal_pos(self, board):
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

    def __check_win_diagonal_neg(self, board):
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

    def __check_draw(self):
        """
        Check if any element with PLAYER.NONE.value exist
        inside the board. 

        Returns:
        - bool: True if the situation is draw
        """
        if np.all((self.__state == 0)) is False:
            is_any_place_left = 0 in self.__state
            return is_any_place_left
        else:
            return False

    def __print_to_board(self):
        """
        Print board to terminal fancier 
        """
        if (self.__mode_game is MODE.TERMINAL_DEBUG) \
            or (self.__mode_game is MODE.RENDER_DEBUG) :
            print(self.__state)

    def __print_player(self):
        """
        Print board to terminal fancier 
        """
        if (self.__mode_game is MODE.TERMINAL_DEBUG) \
            or (self.__mode_game is MODE.RENDER_DEBUG) :
            print("TURN :   {0}".format(self.__PLAYER))

    def __print_situation(self, situation):
        if (self.__mode_game is MODE.TERMINAL_DEBUG) \
            or (self.__mode_game is MODE.RENDER_DEBUG) :
            print("PLAYER : {0} is WON! (vertical check)".format(situation))

    def create_game_board(self):
        """
        Returns game board as np array

        Returns:
        - board (np.ndarray): Numpy array represents game board with size
            __NUM_ROWS X __NUM_COLS
        """
        return np.zeros((self.__NUM_ROWS, self.__NUM_COLS))

    def is_action_valid(self, action):
        """
        Check if the action lies in the action space
        """
        if action >= 0 and action <= self.__NUM_COLS - 1:
            return True

    def make_state(self, player):
        state_dict = {
            'board':self.__state,
            'player' : self.__PLAYER
        }
        return state_dict

    def get_player_by_move(self, move):
        if move == PLAYER.FIRST.value:
            return PLAYER.FIRST
        elif move == PLAYER.SECOND.value:
            return PLAYER.SECOND
        else:
            return PLAYER.NONE

    def get_random_action(self):
        return 1

    def get_action_from_terminal(self):
        action = input('enter the number of row, starting from 0 to N : ')
        return int(action)

    def get_valid_actions(self, action):
        """
        Check if the action lies in the action space
        """
        pass

    def render(self):
        pass

    def reset(self):
        self.__state = self.create_game_board()
        return self.__state
    
    def step(self, action):
        reward = -1
        is_done = False
        state = None

        self.__print_player()

        # Play the game if action is make sense
        if self.is_action_valid(action):
            # In Human mode, its very common for humans to act very stupidly
            # so we need to check again if reference column is really exist, lol
            is_row_found = self.__place_stone(action)

            # Only check action if humans act sensible
            if is_row_found is True:

                # Check if the move is the winning move
                game_result, player = self.__check_win()

                # Evaulate resulted move : How is the game resulted ? : WON,DRAW or NOT_FINISHED ...
                # Thanks to game results also obtain gym info
                state, is_done, reward = self.__evaulate_action_result(player,game_result)

                self.__flip_players()
                self.__print_to_board()
            else:
                print('\n!!!!! WARNING !!!!!')
                print('Given row is already occupied! Please select an occupied')
                print('BTW do you really know how to play this game ?')
                print('---------------------------------------------------------------')

        # ABORT GAME
        else:
            print('Invalid ACTION SELECTED GOD SAKE! ABORT MISSON')
            print('I REPEAT ABORT MI')
            state = None
            reward = None
            is_done = None

        return state, reward, is_done