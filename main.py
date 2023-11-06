import pygame
import random
from GameArea import GameArea
from Tetromino import Tetromino
from constants import BLOCK_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, TetrominoShape, TetrominoColor, WHITESPACE

# Initialize PyGame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Function to draw the game area and tetrominoes
def draw_game():
    for y, row in enumerate(game_area.grid):
        for x, cell_color in enumerate(row):
            pygame.draw.rect(screen, cell_color, (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    
    for y, row in enumerate(current_tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, current_tetromino.color, 
                                ((current_tetromino.x + x)*BLOCK_SIZE, (current_tetromino.y + y)*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

CELL_SIZE = 30  # size of one square cell, you can adjust this as needed

def draw_game_area(surface, game_area):
    for y, row in enumerate(game_area.grid):
        for x, cell_color in enumerate(row):
            if cell_color:
                pygame.draw.rect(surface, cell_color, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(surface, (200, 200, 200), (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)  # grid lines

def draw_tetromino(surface, tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, tetromino.color, ((x+tetromino.x)*CELL_SIZE, (y+tetromino.y)*CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Game variables
game_area = GameArea()
current_tetromino = Tetromino(random.choice(list(TetrominoShape)))
running = True

clock = pygame.time.Clock()
drop_timer = 0
drop_time = 500  # milliseconds, controls how fast the tetromino falls
# Game loop
while running:
    screen.fill(WHITESPACE)
    current_time = pygame.time.get_ticks()
    # Input Handling for lateral movement and rotation
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if game_area.is_valid_move(current_tetromino, -1, 0):
                    current_tetromino.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                if game_area.is_valid_move(current_tetromino, 1, 0):
                    current_tetromino.move(1, 0)
            elif event.key == pygame.K_UP:
                current_tetromino.rotate()
            elif event.key == pygame.K_DOWN:
                drop_time = 100  # Increase drop speed when the down key is pressed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                drop_time = 500
    # Automatic Downward Movement
    if current_time - drop_timer > drop_time:
        if game_area.is_valid_move(current_tetromino, 0, 1):
            current_tetromino.move(0, 1)
        else:  # If can't move down, fix the tetromino and create a new one
            game_area.add_tetromino(current_tetromino)
            current_tetromino = Tetromino(random.choice(list(TetrominoShape)))
            if game_area.game_over(current_tetromino): # Check game over condition
                running = False  # End the game if it's over
        drop_timer = current_time
    
    # Clearing Rows
    game_area.clear_rows()

    # Draw game area and current Tetromino
    draw_game_area(screen, game_area)
    draw_tetromino(screen, current_tetromino)
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
