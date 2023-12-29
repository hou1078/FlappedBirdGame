import pygame
import toml 
from event import BIRD_CLEARED_PIPE

try:
    config = toml.load('config.toml')
except FileNotFoundError:
    config = {}

HEIGHT = config.get('height', 600)
PIPE_SPEED = config.get('pipe_speed', 3)
PIPE_COLOR = tuple(config.get('pipe_color', [0, 180, 0]))

class Pipe(pygame.sprite.Sprite):
    def __init__(self, position, width, height, inverted=0):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.mask = pygame.mask.from_surface(self.image)
        self.image.fill(PIPE_COLOR)
        self.rect = self.image.get_rect()

        if inverted == 0:
            self.rect.bottom = HEIGHT
        elif inverted == 1:
            self.rect.top = 0
        else:
            raise ValueError("Inverted value must be 0 or 1")

        self.rect.x = position

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.right < 0:
            self.kill()
            pygame.event.post(pygame.event.Event(BIRD_CLEARED_PIPE))

