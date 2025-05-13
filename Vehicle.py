import pygame
import config as c
from pygame.math import Vector2

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, vehicle_id, road_coord):
        pygame.sprite.Sprite.__init__(self)
        self.emergency = True if vehicle_id == 2 else False
        sprites = []
        if (vehicle_id == 2):
            sprites.append(pygame.image.load('images/response_police/police_red.png'))
            sprites.append(pygame.image.load('images/response_police/police_blue.png'))
        else:
            path = "images/" + c.vehicleTypes[vehicle_id] + ".png"
            sprites.append(pygame.image.load(path))
        self.current_sprite = 0
        self.ori_image = sprites.copy()
        self.direction_image = sprites.copy()
        self.image = self.direction_image[self.current_sprite]
        self.image_pos = self.image.get_rect()
        self.waypoints = road_coord
        self.waypoint_index = 0
        self.speed = 2
        self.target = self.waypoints[self.waypoint_index]
        self.image_pos.x = self.target[0] + 3
        self.image_pos.y = self.target[1] + 3
        self.pos = Vector2((self.target[0] + 3, self.target[1] + 3))
        self.target_radius = 50

    def flash_light(self):
        self.current_sprite += 0.15
        if int(self.current_sprite) >= len(self.direction_image):
            self.current_sprite = 0
        self.image = self.direction_image[int(self.current_sprite)]

    def render(self, screen):
        screen.blit(self.image, self.image_pos)

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
            self.vel = heading * (distance / self.target_radius * self.speed)
        else:  # Otherwise move with max_speed.
            self.vel = heading * self.speed
        self.pos += self.vel
        self.image_pos.center = self.pos

    def isEmergency(self):
        return self.emergency

    def get_object(self):
        return self

    def get_pos(self):
        return self.image_pos