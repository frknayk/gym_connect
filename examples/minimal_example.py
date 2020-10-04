#!/usr/bin/env python3
import numpy as np
import gym
import gym_connect

env = gym.make('connect-v0') 
state = env.reset()

is_done = False
while not is_done:
    # Comment out the line below for disabling render
    env.render()
    action = env.get_random_action()
    next_state, reward, is_done = env.step(action)
env.close_renderer()