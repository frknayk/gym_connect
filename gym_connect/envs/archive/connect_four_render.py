#!/usr/bin/python3

import gym
from gym import error, spaces, utils
from gym.utils import seeding

import numpy as np
import sys
import math
import pygame

from enums.player import PLAYER
from enums.run_mode import MODE, PLAY_MODE
from enums.results_enum import RESULTS
from enums.colors import Colors

from gym_connect.envs.connect_four_no_render import ConnectHeadless

class ConnectPyGame(ConnectHeadless):
    def __init__(self,number_of_rows=6, number_of_cols=7,
                game_mode = PLAY_MODE.HUMAN_VS_HUMAN):
        pygame.init()
        self.NUM_ROWS = number_of_rows
        self.NUM_COLS = number_of_cols
        self.OFFSET = 200
        self.SQUARE_SIZE = 100
        self.WIDTH = self.NUM_COLS * self.SQUARE_SIZE
        self.HEIGHT = self.NUM_ROWS * self.SQUARE_SIZE + int(self.OFFSET)
        self.RADIUS = int(self.SQUARE_SIZE/2 - 5)
        self.screen = self.__set_screen()
        self.font = pygame.font.SysFont("Comic Sans MS", int(self.OFFSET/4))

    def __set_screen(self):
        """
        Set screen with size WIDTH x HEIGHT
        """
        return pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def __update_pygame(self):
        """
        Update game display after some changes on pygame object
        """
        pygame.display.update()

    def __draw_board(self, board):
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

        self.__update_pygame()

    def __move(self, player, positions):
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

    def __move_mouse(self, posx, player_turn):
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

    def __print_to_board(self, text, color):
        text_surface = self.font.render(text, False, color)
        self.screen.blit(text_surface, (0, 0))
    
