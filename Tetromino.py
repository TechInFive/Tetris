from constants import GAME_WIDTH, TetrominoShape, TetrominoColor

class Tetromino:
    def __init__(self, tetrominoShape):
        self.shape, color_enum = tetrominoShape.value
        self.color = color_enum.value
        self.x = GAME_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
        
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        self.shape = [[self.shape[y][x] for y in range(len(self.shape))] for x in range(len(self.shape[0]) - 1, -1, -1)]
