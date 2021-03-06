#!/usr/bin/python3
import numpy as np
import pygame
import sys
import math
from gym_connect.envs.enums.colors import Colors
from gym_connect.envs.enums.player import PLAYER
from gym_connect.envs.enums.run_mode import MODE

class Renderer:
    def __init__(self, number_of_rows=6, number_of_cols=7, game_mode=MODE.RENDER_NO_DEBUG):
        self.NUM_ROWS = number_of_rows
        self.NUM_COLS = number_of_cols
        self.OFFSET = 200
        self.SQUARE_SIZE = 100
        self.WIDTH = self.NUM_COLS * self.SQUARE_SIZE
        self.HEIGHT = self.NUM_ROWS * self.SQUARE_SIZE + int(self.OFFSET)
        self.RADIUS = int(self.SQUARE_SIZE/2 - 5)
        pygame.init()
        self.screen = self.set_screen()
        self.font = pygame.font.SysFont("Comic Sans MS", int(self.OFFSET/4))

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

    def close(self):
        pygame.time.wait(3000)
        sys.exit()
