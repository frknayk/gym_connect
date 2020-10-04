#!/usr/bin/env python3
import numpy as np
import gym
import gym_connect

env = gym.make('connect-v0') 
state = env.reset()

is_done = False
while not is_done:
    action = env.get_random_action()
    next_state, reward, is_done = env.step(action)
    
print("Winning player : ",next_state['player'].name)
print(next_state['board'])
