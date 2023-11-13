import random

from Tetromino import Tetromino
from constants import TetrominoShape


class InfoArea:
    def __init__(self):
        self.next_tetromino = self.generate_new_tetromino()
        self.score = 0
        self.level = 1
         # Increase level every 100 points
        self.level_up_score = 100
        # Initial drop time in milliseconds
        self.drop_time = 500 
        self.level_up_animation = False
        self.animation_frames = 0

    def generate_new_tetromino(self):
        return Tetromino(random.choice(list(TetrominoShape)))

    def update_score(self, points):
        self.score += points

        new_level = self.score // self.level_up_score + 1
        if new_level > self.level:
            self.level = new_level
            self.drop_time = max(100, 500 - (self.level - 1) * 50)
            self.start_level_up_animation()

    def pull_tetromino(self):
        next_tetromino = self.next_tetromino
        self.next_tetromino = self.generate_new_tetromino()
        return next_tetromino

    def start_level_up_animation(self):
        self.level_up_animation = True
        self.animation_frames = 30  # Animate over 30 frames

    def continue_level_up(self):
        self.animation_frames -= 1
        if self.animation_frames <= 0:
           self.level_up_animation = False

