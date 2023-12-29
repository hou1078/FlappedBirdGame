import pygame

WIDTH = 800
HEIGHT = 600
BGCOLOR = (200, 200, 200)
MAX_VSPEED = 3
JUMP_BOOST = 10
PIPE_SPEED = 3
PIPE_COLOR = (0, 180, 0)


BIRD_HIT_PIPE = pygame.event.custom_type()
BIRD_CLEARED_PIPE = pygame.event.custom_type()
GAME_OVER = pygame.event.custom_type()


HIGH_SCORE_FILE = 'high_score.txt'
