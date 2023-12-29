import pygame
import toml  
from event import GAME_OVER

try:
    config = toml.load('config.toml')
except FileNotFoundError:
    config = {}

MAX_VSPEED = config.get('max_vspeed', 3)
HEIGHT = config.get('height', 600)

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("images/bird.png"), (100, 100)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (50, HEIGHT // 2) 
        self.vspeed = 0
        self.lives = 3

    def update(self):
        self.vspeed = min(MAX_VSPEED, self.vspeed + 1)
        self.rect.y = self.rect.y + self.vspeed

        if self.rect.bottom > HEIGHT:
            self.reset_position()
            self.decrement_lives()

        if self.rect.top < 0:
            self.rect.top = 0
            self.vspeed = 0

    def reset_position(self):
        # Reset the bird's position
        self.rect.center = (50, HEIGHT // 2)
        self.vspeed = 0

    def decrement_lives(self):
        self.lives -= 1
        if self.lives <= 0:
            pygame.event.post(pygame.event.Event(GAME_OVER))
