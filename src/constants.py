

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------------------------------------------------------------------------------------------------

PLAYER_1_IDENTIFIER = 1
PLAYER_2_IDENTIFIER = -1


# AI Training Constants
AI_TESTING_GAMES = 25

# ----------------------------------------------------------------------------------------------------------------------

# Graphics Constants
FRAME_RATE = 60
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_GREEN = (0, 255, 0)

PLAYER_1_COLOR = COLOR_YELLOW
PLAYER_2_COLOR = COLOR_RED

# Game Board
BOARD_CENTER_X = int(WINDOW_WIDTH / 2)
BOARD_CENTER_Y = int(WINDOW_HEIGHT / 2)
CELL_SIZE = 75
NUM_ROWS = 6
NUM_COLS = 7
WIN_COUNT = 4
