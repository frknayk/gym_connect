# Connect4 Environment With PyGame

## Description
- Connect4 environment with two option : 'PyGame Mode' (for renders) and 'Headless Mode' for terminal only.

## Installation
1. Run the command below
   - ``` pip3 install -e . ```

## Info
- State information is a dictionary such that includes board state and the player at that state.
- For using renderer, add ```env.render()``` to the beginning of the loop, do not forget to
close it after the game is done via ```env.close_renderer()```. Check the example *examples/minimal_example* here.
- **Game Modes** : Check the game enumerations here : ```gym_connect.envs.enums.run_mode ```
- **Enable Debug Mode** : 
   ```
   from gym_connect.envs.enums.run_mode import MODE
   env.mode_game = MODE.TERMINAL_DEBUG
   ```

## Usage
1. Simplest usage
   ``` 
   import gym
   import gym_connect 
   env = gym.make('connect-v0') 
   state = env.reset()
   print(state)
   ```
2. Please check */examples* folder for playing with terminal and rendering examples

## Quick Look
<img width=350px height=416px src="images\gym_connect_output.png" alt="Project logo">

## Optional
There is also human to human mode rendered here, run the script below
- ```connect_four_pygame_mouse.py``` 

## Prerequisites
   1. gym
   2. pygame 
   3. numpy
