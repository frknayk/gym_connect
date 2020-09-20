import gym
import gym_connect

env = gym.make('connect-v0')

state = env.reset()
MAX_EPISODES = 100
MAX_STEPS = 100
for eps in range(MAX_EPISODES): 
    for step in range(MAX_STEPS):
        action = env.get_action_from_terminal()
        next_state,reward,done = env.step(action)
