import pygame


class Textbox(pygame.sprite.Sprite):
    def __init__(self, dimensions, color, bgcolor, text, font_size=24):
        super().__init__()
        self.dimensions = dimensions
        self.color = color
        self.bgcolor = bgcolor
        self.font_size = font_size

        self._text = text
        self.update()

        self.rect = self.image.get_rect()
        

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        self._text = str(value)
        self.update()

    def update(self):
        surface = pygame.Surface(self.dimensions)
        surface.fill(self.bgcolor)

        font = pygame.font.SysFont("Arial", self.font_size)
        text_surface = font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect()
        left = self.dimensions[0] / 2 - text_rect.width / 2
        top = self.dimensions[1] / 2 - text_rect.height / 2
        surface.blit(text_surface, (left, top))
        self.image = surface