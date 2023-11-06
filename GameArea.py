from constants import GAME_HEIGHT, GAME_WIDTH, CellState

class GameArea:
    def __init__(self):
        self.width = GAME_WIDTH
        self.height = GAME_HEIGHT
        self.grid = [[CellState.EMPTY.value for _ in range(GAME_WIDTH)] for _ in range(GAME_HEIGHT)]

    def add_tetromino(self, tetromino):
        for y, row in enumerate(tetromino.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[y + tetromino.y][x + tetromino.x] = tetromino.color

    def is_valid_move(self, tetromino, dx, dy):
        for y, row in enumerate(tetromino.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = x + tetromino.x + dx
                    new_y = y + tetromino.y + dy
                    if new_x < 0 or new_x >= self.width or new_y >= self.height or new_y < 0:
                        return False
                    if self.grid[new_y][new_x]:
                        return False
        return True

    def clear_rows(self):
        # Find completed rows
        cleared_rows_indices = [i for i, row in enumerate(self.grid) if all(row)]
        num_cleared = len(cleared_rows_indices)
        
        # If no rows were cleared, just return
        if num_cleared == 0:
            return 0
        
        # For each cleared row index, move every row above it one step down
        for idx in reversed(cleared_rows_indices):
            del self.grid[idx]
            self.grid.insert(0, [0 for _ in range(self.width)])
        
        return num_cleared

    def game_over(self, tetromino):
        for y, row in enumerate(tetromino.shape):
            for x, cell in enumerate(row):
                if cell and self.grid[y + tetromino.y][x + tetromino.x]:
                    return True
        return False
