# Connect4 Environment With PyGame

## Description
- Connect4 environment with two option : 'PyGame Mode' (for renders) and 'Headless Mode' for terminal only.

## Installation
1. Run the command below
   - ``` pip install -e . ```

## Usage
1. Simplest usage
   ``` 
   import gym
   import gym_connect 
   env = gym.make('connect-v0') 
   state = env.reset()
   print(state)
   ```
   
## Optional
There is also human to human mode rendered here, run the script below
- ```connect_four_pygame_mouse.py``` 

## Prerequisites
   1. gym
   2. pygame 
   3. numpy
