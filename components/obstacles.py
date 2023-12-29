import pygame
import csv
from .pipe import Pipe
from pathlib import Path

class Obstacles(pygame.sprite.Group):
    def __init__(self, level_file):
        super().__init__()
        self.load_level(level_file)

    def load_level(self, level_file):
        if not Path(level_file).exists():
            return

        with open(level_file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                position, width, height, inverted = map(int, row)
                self.add(Pipe(position, width, height, inverted))



    def update(self):
        super().update()
        self.remove([pipe for pipe in self.sprites() if pipe.rect.right < 0])
        

    def empty(self) -> None:
        return super().empty()
    
    
