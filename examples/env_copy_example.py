#!/usr/bin/env python3
import numpy as np
import gym
import gym_connect

env = gym.make('connect-v0')
state = env.reset()

env_digital_twin = env.copy() 

next_state_digital_twin, r, d = env_digital_twin.step(1)

print("Original state", env.state)
print("Digital twin state", env_digital_twin.state)

print("TEST - 2 : Change original and take a look if the copied one is alos changed")
env.step(5)
print("Original state", env.state)
print("Digital twin state", env_digital_twin.state)

