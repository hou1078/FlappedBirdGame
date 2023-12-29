import pygame
import pygame.font

class Button:
    def __init__(self, position, color, bgcolor, text, font_size=24):
        pygame.font.init()
        self.rect = pygame.Rect(position, (150, 50))
        self.color = color
        self.bgcolor = bgcolor
        self.text = text
        self.font_size = font_size
        self.update()

    def update(self):
        pygame.font.init()
        font = pygame.font.Font(None, self.font_size)
        text_surface = font.render(self.text, True, self.color, self.bgcolor)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.bgcolor)
        self.image.blit(text_surface, (self.rect.width // 2 - text_surface.get_width() // 2, self.rect.height // 2 - text_surface.get_height() // 2))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
