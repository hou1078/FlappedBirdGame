import pygame
from .base import BaseScreen
from .button import Button
import toml  
try:
    config = toml.load('config.toml')
except FileNotFoundError:
    config = {}

# Use config values in the WelcomeScreen class
WIDTH = config.get('width', 800)
HEIGHT = config.get('height', 600)

class WelcomeScreen(BaseScreen):
    def __init__(self, window, persistent=None):
        super().__init__(window, persistent)
        self.title_font = pygame.font.SysFont(None, 48)
        self.button_start = Button(
            position=(WIDTH // 2 - 75, HEIGHT // 2),
            color=(255, 255, 255),
            bgcolor=(0, 0, 0),
            text="Start",
            font_size=24,
        )

    def update(self):
        self.button_start.update()

    def draw(self):
        self.window.fill(config.get('bgcolor', (200, 200, 200)))
        title_surface = self.title_font.render("Flappy Bird", True, (0, 0, 0))
        self.window.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 100))
        self.button_start.draw(self.window)

    def handle_mouse_click(self, event):
        if event.button == 1:
            if self.button_start.rect.collidepoint(event.pos):
                self.next_screen = "game"
                self.running = False
