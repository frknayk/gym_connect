from enum import Enum

class MODE(Enum):
    NONE = -1
    # Print board or necessary information to terminal
    TERMINAL_DEBUG = 1
    # Do not print, only play like a pyhsco
    TERMINAL_NO_DEBUG = 2
    # Render board, and print necessary info to terminal 
    RENDER_DEBUG = 3
    # Render board, dont print anything to anywhere
    RENDER_NO_DEBUG = 4

class PLAY_MODE(Enum):
    NONE = -1
    HUMAN_VS_HUMAN = 1
    HUMAN_VS_AI = 2
    AI_VS_AI = 3