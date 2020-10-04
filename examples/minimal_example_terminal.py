#!/usr/bin/env python3
import numpy as np
import gym
import gym_connect

env = gym.make('connect-v0') 
state = env.reset()

is_done = False
while not is_done:
    action = env.get_action_from_terminal()
    next_state, reward, is_done = env.step(action)
    
