#!/usr/bin/python3

import gym
from gym import error, spaces, utils
from gym.utils import seeding

import numpy as np
import sys
import math

from enums.player import PLAYER
from enums.run_mode import MODE, PLAY_MODE
from enums.results_enum import RESULTS

from gym_connect.envs.connect_four_pygame_mouse import ConnectPyGame
from gym_connect.envs.connect_four_no_render import ConnectHeadless

class ConnectEnv(gym.Env):
    def __init__(self, number_of_rows=6, number_of_cols=7,
                game_mode=MODE.TERMINAL_DEBUG, play_mode = PLAY_MODE.HUMAN_VS_HUMAN):
        self.__NUM_ROWS = number_of_rows
        self.__NUM_COLS = number_of_cols
        self.__mode_game = game_mode
        self.__mode_play = play_mode
        self.state_dim = self.__NUM_ROWS * self.__NUM_COLS
        self.action_dim = 1
        self.__env = None
        self.__set_connect_env()
    
    def __set_connect_env(self):
        if (self.__mode_game is MODE.RENDER_DEBUG) or \
            (self.__mode_game is MODE.RENDER_NO_DEBUG):
            self.__env = ConnectPyGame(self.__NUM_ROWS,self.__NUM_COLS)
        elif (self.__mode_game is MODE.TERMINAL_DEBUG) or \
            (self.__mode_game is MODE.TERMINAL_NO_DEBUG):
            self.__env = ConnectHeadless(self.__NUM_ROWS,self.__NUM_COLS)
        else:
            print('WRONG GAME MODE IS GIVEN!')
            sys.exit()

    def step(self, action):
        return self.__env.step(action)
    
    def reset(self):
        self.__env.reset()
        
    def render(self, mode='human', close=False):
        pass
    
    def get_action_from_terminal(self):
        return self.__env.get_action_from_terminal()

if __name__ == "__main__":
    env = ConnectEnv(number_of_rows=6,number_of_cols=7,game_mode=MODE.TERMINAL_DEBUG)
    state = env.reset()
    MAX_EPISODES = 100
    MAX_STEPS = 100
    for eps in range(MAX_EPISODES): 
        for step in range(MAX_STEPS):
            action = env.get_action_from_terminal()
            next_state,reward,done = env.step(action)
