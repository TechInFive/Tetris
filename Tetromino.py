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

    def rotate(self, game_area):
        # Create a copy of the current shape to rotate
        new_shape = [[self.shape[y][x] for y in range(len(self.shape))] for x in range(len(self.shape[0]) - 1, -1, -1)]

        # Calculate the new position after rotation
        new_x = self.x
        new_y = self.y

        # Check if the new shape is within the game area boundaries
        for y, row in enumerate(new_shape):
            for x, cell in enumerate(row):
                if cell:
                    if (new_x + x < 0 or new_x + x >= game_area.width or 
                        new_y + y < 0 or new_y + y >= game_area.height):
                        return  # Do not rotate if it goes out of bounds

        # Update shape and position if rotation is valid
        self.shape = new_shape
