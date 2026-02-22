import threading
import pygame
import config as c

class LoadingScreen:
    def __init__(self):
        self.progress = 0
        self.done = False
        self.message = "Starting..."
        self._lock = threading.Lock()

    def set_progress(self, value, message=""):
        with self._lock:
            self.progress = value
            if message:
                self.message = message

    def mark_done(self):
        with self._lock:
            self.done = True

    def draw(self, surface):
        surface.fill((30, 30, 40))

        font = pygame.font.SysFont(None, 36)
        text = font.render(self.message, True, (255, 255, 255))
        surface.blit(text, (c.SCREEN_WIDTH  // 2 - text.get_width() // 2, c.SCREEN_HEIGHT // 2 - 80))

        # Bar background
        bar_width = 500
        bar_height = 40
        x = c.SCREEN_WIDTH // 2 - bar_width // 2
        y = c.SCREEN_HEIGHT // 2

        pygame.draw.rect(surface, (80, 80, 80), (x, y, bar_width, bar_height), border_radius=8)

        # Progress fill
        fill_width = int(bar_width * (self.progress / 100))
        pygame.draw.rect(surface, (0, 200, 100), (x, y, fill_width, bar_height), border_radius=8)

        percent_text = font.render(f"{self.progress}%", True, (255, 255, 255))
        surface.blit(percent_text, (c.SCREEN_WIDTH  // 2 - percent_text.get_width() // 2, y + 50))