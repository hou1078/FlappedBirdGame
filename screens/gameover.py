import pygame
from .base import BaseScreen
from .button import Button
import toml 

try:
    config = toml.load('config.toml')
except FileNotFoundError:
    config = {}

WIDTH = config.get('width', 800)
HEIGHT = config.get('height', 600)

class GameOverScreen(BaseScreen):
    def __init__(self, window, persistent=None):
        super().__init__(window, persistent)
        self.title_font = pygame.font.SysFont(None, 48)
        self.button_play_again = Button(
            position=(WIDTH // 2 - 75, HEIGHT // 2 - 50),
            color=(255, 255, 255),
            bgcolor=(0, 0, 0),
            text="Play Again",
            font_size=24,
        )
        self.button_quit = Button(
            position=(WIDTH // 2 - 75, HEIGHT // 2 + 50),
            color=(255, 255, 255),
            bgcolor=(0, 0, 0),
            text="Quit",
            font_size=24,
        )

    def update(self):
        self.button_play_again.update()
        self.button_quit.update()

    def draw(self):
        self.window.fill(config.get('bgcolor', (200, 200, 200)))
        title_surface = self.title_font.render("Game Over", True, (0, 0, 0))
        self.window.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 100))
        if 'points' in self.persistent:
            score_surface = self.title_font.render(f"Score: {self.persistent['points']}", True, (0, 0, 0))
            self.window.blit(score_surface, (WIDTH // 2 - score_surface.get_width() // 2, 200))
        self.button_play_again.draw(self.window)
        self.button_quit.draw(self.window)

    def handle_mouse_click(self, event):
        if event.button == 1:
            if self.button_play_again.rect.collidepoint(event.pos):
                self.next_screen = "game"
                self.running = False
            elif self.button_quit.rect.collidepoint(event.pos):
                self.next_screen = None
                self.running = False
                quit()
