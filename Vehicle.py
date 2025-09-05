import pygame
from random import randint
from pygame.math import Vector2
import networkx as nx

from drivable_road import DrivableRoad


class BaseVehicle(pygame.sprite.Sprite):
    def __init__(self, sprites):
        super().__init__()
        self.current_sprite = 0
        self.ori_image = sprites.copy()
        self.direction_image = sprites.copy()
        self.image = self.direction_image[self.current_sprite]
        self.image_pos = self.image.get_rect()
        self.drivable_road = DrivableRoad()
        self.start_node = self.drivable_road.get_random_node()
        self.end_node = self.drivable_road.get_random_node()
        self.path = self.drivable_road.get_path(self.start_node, self.end_node)
        self.speed = 1
        self.image_pos.x = self.path[0][0] + 1
        self.image_pos.y = self.path[0][1] + 1
        self.pos = Vector2(self.path[0])
        self.target_radius = 50
        self.vel = Vector2(0, 0)
        self.current_index = 0

    def flash_light(self):
        pass

    def render(self, screen):
        screen.blit(self.image, self.image_pos)

    def get_safe_path(self):
        while True:
            self.end_node = self.drivable_road.get_random_node()
            try:
                self.path = self.drivable_road.get_path(self.start_node, self.end_node)
                break
            except nx.NetworkXNoPath:
                continue

    def update(self):
        # If we've reached the end of the path, pick a new route
        if self.current_index >= len(self.path) - 1:
            self.start_node = self.end_node
            self.get_safe_path()
            self.current_index = 0
            self.pos = pygame.Vector2(self.path[0])

        # Current target waypoint
        target = pygame.Vector2(self.path[self.current_index + 1])
        heading = target - self.pos
        distance = heading.length()

        if distance < 1:  # close enough → go to next waypoint
            self.current_index += 1
            return

        heading.normalize_ip()

        if distance <= self.target_radius and self.current_index == len(self.path) - 2:
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
