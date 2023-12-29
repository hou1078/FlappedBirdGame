import pygame

class BaseScreen:
    def __init__(self, window, persistent=None):
        if persistent is None:
            self.persistent = {}
        else:
            self.persistent = persistent

        self.window = window
        self.next_screen = None
        self.running = False

    def run(self):
        clock = pygame.time.Clock()
        self.running = True
        while self.running:
            clock.tick(60)
            events = pygame.event.get()
            self.manage_events(events)
            self.update()
            self.draw()
            pygame.display.update()

    def manage_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                self.next_screen = None
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
                self.next_screen = None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event)

    def handle_mouse_click(self, event):
        pass