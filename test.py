import pygame as pg
from pygame.math import Vector2

class Entity(pg.sprite.Sprite):

    def __init__(self, pos, waypoints):
        super().__init__()
        self.image = pg.Surface((30, 50))
        self.image.fill(pg.Color('dodgerblue1'))
        self.rect = self.image.get_rect(center=pos)
        self.vel = Vector2(0, 0)
        self.max_speed = 3
        self.pos = Vector2(pos)
        self.waypoints = waypoints
        self.waypoint_index = 0
        self.target = self.waypoints[self.waypoint_index]
        self.target_radius = 50

    def update(self):
        # A vector pointing from self to the target.
        heading = self.target - self.pos
        distance = heading.length()  # Distance to the target.
        heading.normalize_ip()
        if distance <= 2:  # We're closer than 2 pixels.
            # Increment the waypoint index to swtich the target.
            # The modulo sets the index back to 0 if it's equal to the length.
            self.waypoint_index = (self.waypoint_index + 1) % len(self.waypoints)
            self.target = self.waypoints[self.waypoint_index]
        if distance <= self.target_radius:
            # If we're approaching the target, we slow down.
            self.vel = heading * (distance / self.target_radius * self.max_speed)
        else:  # Otherwise move with max_speed.
            self.vel = heading * self.max_speed

        self.pos += self.vel
        self.rect.center = self.pos


def main():
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    waypoints = [(200, 100), (500, 400), (100, 300)]
    all_sprites = pg.sprite.Group(Entity((100, 300), waypoints))
    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
        all_sprites.update()
        screen.fill((0))
        all_sprites.draw(screen)
        for point in waypoints:
            pg.draw.rect(screen, (90, 200, 40), (point, (4, 4)))
        pg.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()