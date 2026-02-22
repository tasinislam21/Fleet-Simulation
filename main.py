import pygame
import argparse
import config as c
from engine import Engine

parser = argparse.ArgumentParser()
parser.add_argument('--number_of_emergency_police', type=int, default=0)
parser.add_argument('--number_of_normal_police', type=int, default=8)
parser.add_argument('--number_civilian_car', type=int, default=20)
parser.add_argument('--number_civilian_bike', type=int, default=8)
args = parser.parse_args()

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

pygame.display.set_caption("Police vehicle simulator")
map_surface = pygame.Surface((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
map_surface.fill((0, 0, 0))


if __name__ == "__main__":
    engine = Engine(args, map_surface, screen)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if engine.get_engine_ready():
            engine.update()
        clock.tick(60)

pygame.quit()