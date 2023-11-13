from enum import Enum, auto

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 450, 600
GAME_WIDTH, GAME_HEIGHT = 10, 20
BLOCK_SIZE = 30
INFO_AREA_START = (320, 50)
INFO_AREA_WIDTH = 120

WHITESPACE = (255, 255, 255)
SCORE_COLOR = (0, 0, 255)

class CellState(Enum):
    EMPTY = 0
    FILLED = auto()  # This would automatically assign the next integer, i.e., 1.

class TetrominoColor(Enum):
    CYAN = (0, 255, 255)
    PURPLE = (255, 0, 255)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    ORANGE = (255, 165, 0)

class TetrominoShape(Enum):
    I = ([[1, 1, 1, 1]], TetrominoColor.CYAN)
    T = ([[1, 1, 1], [0, 1, 0]], TetrominoColor.PURPLE)
    O = ([[1, 1], [1, 1]], TetrominoColor.YELLOW)
    S = ([[0, 1, 1], [1, 1, 0]], TetrominoColor.GREEN)
    Z = ([[1, 1, 0], [0, 1, 1]], TetrominoColor.RED)
    J = ([[1, 0, 0], [1, 1, 1]], TetrominoColor.BLUE)
    L = ([[0, 0, 1], [1, 1, 1]], TetrominoColor.ORANGE)
