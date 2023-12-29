import pygame
from pathlib import Path
from screens.welcome import WelcomeScreen
from screens.gameover import GameOverScreen
from screens.game import GameScreen
import pygame.font
import toml  

try:
    config = toml.load('config.toml')
except FileNotFoundError:
    config = {}

WIDTH = config.get('width', 800)
HEIGHT = config.get('height', 600)

def main():
    pygame.init()
    pygame.font.init()
    pygame.key.set_repeat(400, 400)
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    screens = {
        "welcome": WelcomeScreen,
        "game": GameScreen,
        "gameover": GameOverScreen,
    }

    current_screen = "welcome"
    current_level = 1
    running = True


    while running:
        pygame.event.pump()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

        if current_screen == "game":
            level_file = f"level{current_level}.csv"
            level_path = Path(__file__).resolve().parent / level_file
            screen = screens[current_screen](window, {"level_path": level_path, "current_level": current_level})
        else:
            screen = screens[current_screen](window)


        screen.manage_events(events)
        screen.run()
        screen.draw()

        if screen.next_screen:
            current_screen = "welcome"
            if screen.next_screen == "game":
                current_screen = "game"
                if hasattr(screen, 'obstacles') and screen.obstacles.empty():
                    current_level += 1
                    screen.handle_next_level()
            elif screen.next_screen == "gameover":
                current_screen = "gameover"
            


    pygame.quit()

if __name__ == "__main__":
    main()
