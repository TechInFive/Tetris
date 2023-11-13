import pygame
from GameArea import GameArea
from InfoArea import InfoArea
from constants import BLOCK_SIZE, INFO_AREA_START, INFO_AREA_WIDTH, SCORE_COLOR, SCREEN_HEIGHT, SCREEN_WIDTH, WHITESPACE

# Initialize PyGame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Game variables
game_area = GameArea()
info_area = InfoArea()
current_tetromino = info_area.pull_tetromino()

land_sound = pygame.mixer.Sound('bottle.cork.wav')
clear_sound = pygame.mixer.Sound('bell.transition.wav')

badge_image = pygame.image.load('star.badge.png')
badge_mask_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
pygame.draw.circle(badge_mask_surface, (255, 255, 255, 255), (15, 15), 13.5)
badge_mask_surface.blit(badge_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

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

def draw_score_bar(surface, info_area, x, y, width, height):
    # draw progress bar
    fill_width = (info_area.score % info_area.level_up_score) / info_area.level_up_score * width
    pygame.draw.rect(surface, (0, 255, 0), (x, y, fill_width, height))
    # draw border
    pygame.draw.rect(surface, (0, 0, 255), (x - 2, y - 2, width + 4, height + 4), 2)

def draw_badges(surface, info_area, start_x, start_y):
    badge_size = 30  # Size of each badge
    badge_spacing = 2  # Space between badges
    badges_per_row = 4
    row_height = badge_size + badge_spacing

    for level in range(1, info_area.level + 1):
        row_number = (level - 1) // badges_per_row
        column_number = (level - 1) % badges_per_row

        badge_x = start_x + column_number * (badge_size + badge_spacing)
        badge_y = start_y + row_number * row_height

        if level < info_area.level or not info_area.level_up_animation or info_area.animation_frames % 5 == 0:
            surface.blit(badge_mask_surface, (badge_x, badge_y))

    if info_area.level_up_animation:
        info_area.continue_level_up()

def draw_info_area(surface, info_area):
    # Draw Next Tetromino
    next_tetromino = info_area.next_tetromino
    tetromino_start_x = INFO_AREA_START[0]
    tetromino_start_y = INFO_AREA_START[1]
    
    for y, row in enumerate(next_tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, next_tetromino.color, 
                                 (tetromino_start_x + x*CELL_SIZE, tetromino_start_y + y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    draw_score_bar(surface, info_area, INFO_AREA_START[0], INFO_AREA_START[1] + 100, INFO_AREA_WIDTH, 20)

    draw_badges(surface, info_area, INFO_AREA_START[0], INFO_AREA_START[1] + 150)

running = True

clock = pygame.time.Clock()
drop_timer = 0
current_drop_time = info_area.drop_time

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
                current_tetromino.rotate(game_area)
            elif event.key == pygame.K_DOWN:
                current_drop_time = info_area.drop_time // 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                current_drop_time = info_area.drop_time

    # Automatic Downward Movement
    if current_time - drop_timer > current_drop_time:
        if game_area.is_valid_move(current_tetromino, 0, 1):
            current_tetromino.move(0, 1)
        else:  # If can't move down, fix the tetromino and create a new one
            game_area.add_tetromino(current_tetromino)
            current_tetromino = info_area.pull_tetromino()
            land_sound.play()
            if game_area.game_over(current_tetromino): # Check game over condition
                running = False  # End the game if it's over
        drop_timer = current_time
    
    # Clearing Rows
    rows = game_area.clear_rows()
    if (rows > 0):
        clear_sound.play()
        info_area.update_score(10 * (2 ** (rows - 1)))
        current_drop_time = info_area.drop_time

    # Draw game/info area and current Tetromino
    draw_game_area(screen, game_area)
    draw_info_area(screen, info_area)
    draw_tetromino(screen, current_tetromino)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()



