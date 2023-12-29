import pygame
from .base import BaseScreen
from pathlib import Path
from components.bird import Bird
from components.obstacles import Obstacles
from components.textbox import Textbox
import toml  
from event import BIRD_CLEARED_PIPE, BIRD_HIT_PIPE, GAME_OVER

try:
    config = toml.load('config.toml')
except FileNotFoundError:
    config = {}

WIDTH = config.get('width', 800)
HEIGHT = config.get('height', 600)
BGCOLOR = tuple(config.get('bgcolor', [200, 200, 200]))
JUMP_BOOST = config.get('jump_boost', 10)
HIGH_SCORE_FILE = config.get('high_score_file', 'high_score.txt')



class GameScreen(BaseScreen):
    def __init__(self, window, persistent):
        super().__init__(window, persistent)
        self.current_level = 1
        self.bird = Bird()
        self.obstacles = Obstacles(f"level{self.current_level}.csv")
        self.persistent = {"points": 0}
        self.load_high_score()
        self.scorebox = Textbox((100, 100), (255, 255, 255), (0, 0, 0), "0", font_size=36)
        self.scorebox.rect.topright = (WIDTH, 0)
        self.high_score_box = Textbox((WIDTH // 2, 50), (255, 255, 255), (0, 0, 0), f"High Score: {self.high_score}", font_size=24)
        self.high_score_box.rect.centerx = WIDTH // 2
        self.lost = False
        self.lost_message = Textbox((200, 200), (255, 0, 0), (0, 0, 0), "FAIL!", font_size=48)
        self.lost_message.rect.center = self.window.get_rect().center
        self.lives_box = Textbox((100, 50), (255, 0, 0), (0, 0, 0), f"Lives: {self.bird.lives}", font_size=24)
        self.level_box = Textbox((100, 50), (255, 0, 0), (0, 0, 0), f"Level: {self.current_level}", font_size=24)

    def load_high_score(self):
        try:
            with open(HIGH_SCORE_FILE, 'r') as file:
                self.high_score = int(file.read())
        except FileNotFoundError:
            self.high_score = 0

    def update_high_score(self):
        if self.persistent["points"] > self.high_score:
            self.high_score = self.persistent["points"]
            with open(HIGH_SCORE_FILE, 'w') as file:
                file.write(str(self.high_score))


    def handle_next_level(self):
        self.current_screen = "game"
        self.current_level += 1
        level_file = f"level{self.current_level}.csv"
        level_file_path = Path(__file__).resolve().parent / level_file


        if level_file_path.exists():
            self.obstacles.empty() 
            self.obstacles.load_level(level_file_path)
            self.bird.reset_position()
            self.next_screen = "game"
        else:
            self.next_screen = "gameover"
            self.running = False

    def update(self):
        self.bird.update()
        self.obstacles.update()

        if pygame.sprite.spritecollide(self.bird, self.obstacles, False, pygame.sprite.collide_mask):

            self.bird.decrement_lives()
            pygame.event.post(pygame.event.Event(BIRD_HIT_PIPE))
            self.obstacles.empty()
            self.bird.reset_position()
            if self.current_level > 1:
                self.obstacles.load_level(f"level{self.current_level-1}.csv")
            else:
                self.obstacles.load_level(f"level{self.current_level}.csv")

            if self.bird.lives > 0:
                self.lives_box.text = f"Lives: {self.bird.lives}"
            else:
                self.update_high_score()
                self.next_screen = "gameover"
                self.running = False
                pygame.event.post(pygame.event.Event(GAME_OVER))

        else:
            if not self.obstacles.sprites():
                self.handle_next_level()

        
    def manage_events(self, events):
        for event in events:
            if not self.lost:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.bird.vspeed = -JUMP_BOOST

                if event.type == BIRD_CLEARED_PIPE:
                    self.persistent["points"] += 1
                    self.update_high_score()
                    self.scorebox.text = str(self.persistent["points"])



    def draw(self):
        self.window.fill(BGCOLOR)

        if not self.lost:
            self.obstacles.draw(self.window)
            self.window.blit(self.bird.image, self.bird.rect)
            self.window.blit(self.scorebox.image, self.scorebox.rect)
            self.window.blit(self.high_score_box.image, self.high_score_box.rect)
            self.lives_box.text = f"Lives: {self.bird.lives}"
            self.level_box.text = f"Level: {self.current_level}"
            self.window.blit(self.lives_box.image, self.lives_box.rect.topleft)
            self.window.blit(self.level_box.image, (0, 50))
        else:
            self.window.blit(self.lost_message.image, self.lost_message.rect)

        pygame.display.flip()
