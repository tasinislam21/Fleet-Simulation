import pygame
from random import randint
from pygame.math import Vector2

from drivable_road import DrivableRoad


class BaseVehicle(pygame.sprite.Sprite):
    def __init__(self, sprites):
        super().__init__()
        self.current_sprite = 0
        self.ori_image = sprites.copy()
        self.direction_image = sprites.copy()
        self.image = self.direction_image[self.current_sprite]
        self.image_pos = self.image.get_rect()
        drivable_road = DrivableRoad()
        self.waypoints = drivable_road.get_drivable_road()
        self.waypoint_index = randint(0, len(self.waypoints) - 1)
        self.speed = 1
        self.target = self.waypoints[self.waypoint_index]
        self.image_pos.x = self.target[0] + 3
        self.image_pos.y = self.target[1] + 3
        self.pos = Vector2((self.target[0] + 3, self.target[1] + 3))
        self.target_radius = 50
        self.vel = Vector2(0, 0)

    def flash_light(self):
        pass

    def render(self, screen):
        screen.blit(self.image, self.image_pos)

    def update(self):
        heading = self.target - self.pos
        distance = heading.length()
        heading.normalize_ip()
        if distance <= 2:
            self.waypoint_index = (self.waypoint_index + 1) % len(self.waypoints)
            self.target = self.waypoints[self.waypoint_index]
        if distance <= self.target_radius:
            self.vel = heading * (distance / self.target_radius * self.speed)
        else:
            self.vel = heading * self.speed
        self.pos += self.vel
        self.image_pos.center = self.pos

    def isEmergency(self):
        return False

    def get_object(self):
        return self

    def get_pos(self):
        return self.image_pos

class Police(BaseVehicle):
    def __init__(self, emergency):
        self.emergency = emergency
        if emergency:
            sprites = [
                pygame.image.load('images/response_police/police_red.png'),
                pygame.image.load('images/response_police/police_blue.png')
            ]
        else:
            sprites = [
                pygame.image.load('images/police.png')
            ]
        super().__init__(sprites)

    def isEmergency(self):
        return self.emergency

    def flash_light(self):
        self.current_sprite += 0.15
        if int(self.current_sprite) >= len(self.direction_image):
            self.current_sprite = 0
        self.image = self.direction_image[int(self.current_sprite)]

class Car(BaseVehicle):
    def __init__(self):
        path = f"images/car.png"
        sprites = [pygame.image.load(path)]
        super().__init__(sprites)

class Bike(BaseVehicle):
    def __init__(self):
        path = f"images/bike.png"
        sprites = [pygame.image.load(path)]
        super().__init__(sprites)

class PoliceFactory:
    @staticmethod
    def create_vehicle(emergency):
        return Police(emergency)


class CarFactory:
    @staticmethod
    def create_vehicle():
        return Car()


class BikeFactory:
    @staticmethod
    def create_vehicle():
        return Bike()
